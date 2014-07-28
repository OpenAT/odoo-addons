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
# Metal Surcharge Type
#----------------------------------------------------------

class product_metal_surcharge_type(osv.osv):

    def _current_rate(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
        date = date or time.strftime('%Y-%m-%d %H:%M:%S')
        for type in self.browse(cr, uid, ids, context=context):
            if type.rate_ids:
                cr.execute("SELECT surcharge_type_id, rate FROM metal_surcharge_rate WHERE surcharge_type_id = %s AND name <= %s ORDER BY name desc, id desc LIMIT 1" ,(type.id, date))
                if cr.rowcount:
                    id, rate = cr.fetchall()[0]
                    res[type.id] = rate
            else:
                res[type.id] = 0
        return res

    def _last_update(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            date = date or time.strftime('%Y-%m-%d %H:%M:%S')
            
        for type in self.browse(cr, uid, ids, context=context):
            if type.rate_ids:
                cr.execute("SELECT surcharge_type_id, name FROM metal_surcharge_rate WHERE surcharge_type_id = %s AND name <= %s ORDER BY name desc, id desc LIMIT 1" ,(type.id, date))
                if cr.rowcount:
                    id, name = cr.fetchall()[0]
                    res[type.id] = name
                else:
                    res[type.id] = name
        return res


    _name = 'product.metal.surcharge.type'
    _description = 'Metal Surcharge Type'
    _columns = {
        'name': fields.char('Surcharge Type', size=64, required=True, translate=True),
        'source_url': fields.char('Source Url', size=250),
        'rate': fields.function(_current_rate, string='DEL Number', digits=(12,4), help='The last updated DEL number.'),
        'rate_ids': fields.one2many('metal.surcharge.rate', 'surcharge_type_id', 'Surcharge Rates'),
        'last_update': fields.function(_last_update, string='Last update', type="datetime", help='The last updated date.'),
    }
product_metal_surcharge_type()

#----------------------------------------------------------
# Metal Surcharge Rate
#----------------------------------------------------------

class metal_surcharge_rate(osv.osv):
    _name = "metal.surcharge.rate"
    _description = "Metal Surcharge Rate"

    _columns = {
        'name': fields.datetime('Date', required=True, select=True),
        'rate': fields.float('Rate', digits=(12,4)),
        'surcharge_type_id': fields.many2one('product.metal.surcharge.type', 'Surcharge Type', readonly=True),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    _order = "name desc"

metal_surcharge_rate()

#----------------------------------------------------------
# Products
#----------------------------------------------------------

class product_product(osv.osv):
    
    def onchange_surcharge_type(self, cr, uid, ids, metal_surcharge_type):
        result ={}
        if metal_surcharge_type:
    
            surcharge_type=self.pool.get('product.metal.surcharge.type').browse(cr,uid,metal_surcharge_type)
            result['del_number_temp']=surcharge_type.rate
            result['del_number']=surcharge_type.rate
            result['last_update_temp']=surcharge_type.last_update
            result['last_update']=surcharge_type.last_update

        return {'value':result}
    
    def _get_del_number(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            if product.del_number:
                res[product.id] = product.del_number
            else:
                res[product.id] = 0.0
        return res
    
    def _get_last_update(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            if product.metal_surcharge_type:
                if product.last_update:
                    res[product.id] = product.last_update
                else:
                    res[product.id] = product.last_update_temp
        return res


    _inherit = 'product.product'
    _columns = {
        'metal_surcharge_type': fields.many2one('product.metal.surcharge.type', 'Type of Surcharge', select=True),
        'metal_number': fields.float('Metal Number', help="e.g. The amount of metal per length inside the cable"),
        'metal_base': fields.float('Metal Base', help="e.g. The additional fee that is already included in the price of the cable"),
        'del_number_temp': fields.function(_get_del_number, string='DEL-Number', type='float', help='The last updated DEL number.'),
        'del_number': fields.float('DEL-Number', digits=(12,4), help='The last updated DEL number.'),
        'last_update_temp': fields.function(_get_last_update, string='Last Update', type='datetime', help='The last updated date.'),
        'last_update': fields.datetime('Last Update', help='The last updated date.'),
    }

product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: