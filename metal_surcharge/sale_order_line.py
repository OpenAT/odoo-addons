# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Binary Quest Limited
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp


#----------------------------------------------------------
# Sale Order Line
#----------------------------------------------------------

class sale_order_line(osv.osv):
    
    def _surcharge_calculation(self, cr, uid, metal_number, metal_base, del_number, qty, context=None):
        context = context or {}
        surcharge_per_unit = (metal_number * (((del_number + 0.01) - metal_base)/100.0))
        surcharge = surcharge_per_unit * qty
        return surcharge
    
    def _subtotal_calculation(self, cr, uid, unit_price=0.0, qty=0.0, dis_amt=0.0, surcharge=0.0, context=None):
        context = context or {}
        val = ((unit_price * qty) - dis_amt + surcharge)            
        return val
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        context = context or {}
        
        res = {}
        res = super(sale_order_line, self)._amount_line(cr, uid, ids, field_name, arg, context)
        
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            taxes['total'] = taxes['total'] + line.surcharge
            taxes['total_included'] = taxes['total_included'] + line.surcharge
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        
        return res
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        context = context or {}
        #print "56", context
        
        result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        
        result['value']['surcharge_invisible'] = True
        
        if product:
            product_obj = self.pool.get('product.product')
            product_obj = product_obj.browse(cr, uid, product, context=context)
            
            price_unit = result['value']['price_unit'] or False            
            
            #Update metal_number, metal_base, last_update, del_number
            result['value']['metal_number'] = product_obj.metal_number
            result['value']['metal_base'] = product_obj.metal_base
            result['value']['last_update'] = product_obj.last_update
            result['value']['del_number'] = product_obj.del_number            
            
            #Surcharge
            surcharge = 0.0
            if product_obj.metal_surcharge_type:
                result['value']['surcharge_invisible'] = False
                surcharge = self._surcharge_calculation(cr, uid, product_obj.metal_number, product_obj.metal_base, product_obj.del_number, qty, context)
                result['value']['surcharge_temp'] = surcharge
                result['value']['surcharge'] = surcharge                
            
            #Discount
            try:
                discount = context['discount'] or False
            except: 
                discount = False
                
            dis_amt = 0.0    
            if discount:                
                dis_amt = ((discount * price_unit * qty)/100.0)
                
            result['value']['discount_amount_temp'] = dis_amt
            result['value']['discount_amount'] = dis_amt   
            
            #Subtotal
            subtotal = self._subtotal_calculation(cr, uid, price_unit, qty, dis_amt, surcharge, context)
            result['value']['sub_total_temp'] = subtotal
            result['value']['sub_total'] = subtotal

        return  result
    
    def onchange_discount(self, cr, uid, ids, discount=0, surcharge=0, qty=0, unit_price=0, context=None):
        #print "discount", discount, "surcharge", surcharge, "qty", qty, "unit_price", unit_price
        #print "ids", ids
        #print "onchange_discount"
        context = context or {}
        result = {'value': {'discount_amount_temp': 0.0,
                            'discount_amount': 0.0,
                            'sub_total_temp':0.0,
                            'sub_total':0.0},
                  }
        
        dis_amt = ((discount * unit_price * qty)/100.0)
        subtotal = self._subtotal_calculation(cr, uid, unit_price, qty, dis_amt, surcharge, context)
        result['value']['discount_amount_temp'] = dis_amt
        result['value']['discount_amount'] = dis_amt
        result['value']['sub_total_temp'] = subtotal
        result['value']['sub_total'] = subtotal
        #print "result",result            
        return  result
    
    def onchange_surcharge(self, cr, uid, ids, product, metal_number=0.0, metal_base=0.0, del_number=0.0, qty=0, unit_price=0.0, dis_amt=0.0, context=None):
        
        #print "onchange_surcharge"
        context = context or {}
        result = {'value': {'surcharge_temp': 0.0,
                            'surcharge': 0.0},
                  }
        if product:
            surcharge = 0.0
            product_obj = self.pool.get('product.product')
            product_obj = product_obj.browse(cr, uid, product, context=context)
            if product_obj.metal_surcharge_type:
                surcharge = self._surcharge_calculation(cr, uid, metal_number, metal_base, del_number, qty, context)
                result['value']['surcharge_temp'] = surcharge
                result['value']['surcharge'] = surcharge
            
            subtotal = self._subtotal_calculation(cr, uid, unit_price, qty, dis_amt, surcharge, context)
            result['value']['sub_total_temp'] = subtotal
            result['value']['sub_total'] = subtotal
                            
        return  result    
    
    def _get_surcharge(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):         
            if line.surcharge:
                res[line.id] = line.surcharge
            else:
                res[line.id] = 0.0    
        return res
    
    def _get_subtotal(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):         
            if line.sub_total:
                res[line.id] = line.sub_total
            else:
                res[line.id] = 0.0    
        return res
    
    def _get_discount(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):         
            if line.discount_amount:
                res[line.id] = line.discount_amount
            else:
                res[line.id] = 0.0    
        return res
    

    _inherit = 'sale.order.line'
    _columns = {
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),        
        'discount': fields.float('Discount (%)', digits_compute= dp.get_precision('Discount'), readonly=True, states={'draft': [('readonly', False)]}),
        'metal_number': fields.float('Metal number', help="e.g. The amount of metal per length inside the cable"),
        'metal_base': fields.float('Metal base', help="e.g. The additional fee that is already included in the price of the cable"),
        'last_update': fields.datetime('Last update', help=""),
        'del_number': fields.float('DEL number', help=""),
        'surcharge_temp': fields.function(_get_surcharge, type='float', string='Surcharge'),
        'surcharge': fields.float('Surcharge', digits=(12,4)),
        'discount_amount_temp': fields.function(_get_discount, string='Discount', type='float', help="The discount amount."),
        'discount_amount': fields.float('Discount', help="The discount amount."),
        'sub_total_temp': fields.function(_get_subtotal, type='float', store=True, string='Subtotal'),
        'sub_total': fields.float('Subtotal', digits=(12,4)),
        'pricelist_id': fields.related('order_id', 'pricelist_id', type="many2one", relation="product.pricelist",  string="Pricelist", readonly=True, help="Pricelist for current sales order."),
        'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency", readonly=True),
        'surcharge_invisible': fields.boolean('Surcharge'),
    }
    _defaults = {
        'surcharge_invisible': 'False',
    }

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: