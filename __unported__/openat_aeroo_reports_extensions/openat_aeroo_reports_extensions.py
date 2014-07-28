# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2013 OpenAT (http://www.openat.at) All Rights Reserved.
#                    General contacts <office@openat.at>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from openerp.osv import osv,fields
from openerp.tools.translate import _
import decimal_precision as dp

EXCLUDE_PRODUCT_NAMES = ("SUBTOTAL", "SUBTOTAL-ALL", "HEADER")

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def action_button_confirm(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        for so in self.browse(cr, uid, ids, context=context):
            if any(filter(lambda l: l.optional, so.order_line)):
                raise osv.except_osv(_('Can not confirm sales order with optional items.'), \
                        _('Make sure there is no items with "Exclude From Total" checked!'))
        return super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)

    def amount_all(s):
        def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
            ctx = context.copy()
            ctx['dont_calc_optional'] = True
            return super(sale_order, self)._amount_all(cr, uid, ids, \
                                        field_name, arg, context=ctx)
        return _amount_all

    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0
        if not line.optional:
            return super(sale_order, self)._amount_line_tax(cr, uid, line, context=context)
        return val

    def __init__(self, pool, cr):
        super(sale_order, self).__init__(pool, cr)
        self._columns['amount_untaxed']._fnct = self.amount_all()
        self._columns['amount_tax']._fnct = self.amount_all()
        self._columns['amount_total']._fnct = self.amount_all()

    _columns = {
	    'openat_salesorder_valid_date' : fields.date('Valid to'),
        'openat_report_incl_image' : fields.boolean('Report show images'),
        'openat_report_incl_description' : fields.boolean('Report show long descriptions')
    }

    _defaults = {
        'openat_report_incl_image': True,
        'openat_report_incl_description': True
    }


class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    def amount_line(s):
        def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
            lines = self.browse(cr, uid, ids, context=context)
            exclude_ids = [l.id for l in lines if l.product_id.name in EXCLUDE_PRODUCT_NAMES]
            if context.get('dont_calc_optional'):
                opt_ids = [o.id for o in lines if o.optional]
                not_opt_ids = [o.id for o in lines if not o.optional and o.id not in exclude_ids]
                result = super(sale_order_line, self)._amount_line(cr, uid, not_opt_ids, \
                                                    field_name, arg, context=context)
                result.update(dict.fromkeys(opt_ids+exclude_ids, 0.0))
            else:
               result = super(sale_order_line, self)._amount_line(cr, uid, list(set(ids)-set(exclude_ids)), \
                                                    field_name, arg, context=context)
               result.update(dict.fromkeys(exclude_ids, 0.0))
            return result
        return _amount_line

    def __init__(self, pool, cr):
        super(sale_order_line, self).__init__(pool, cr)
        self._columns['price_subtotal']._fnct = self.amount_line()

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        ret = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=False, context=None)
        ret['hide_price'] = line.hide_price
        ret['hide_subtotal'] = line.hide_subtotal
        return ret

    _columns = {
        'optional': fields.boolean('Exclude from Total', readonly=False, help='Exclude from Total'),
        'hide_price':fields.boolean('Hide', required=False, help='Hide in Report'),
        'hide_subtotal':fields.boolean('Exclude from Subtotal', required=False, help='Exclude from Subtotal'),
    }
    
class account_invoice_line(osv.osv):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    _columns = {
        'hide_price':fields.boolean('Hide', required=False, help='Hide in Report'),
        'hide_subtotal':fields.boolean('Exclude from Subtotal', required=False, help='Exclude from Subtotal'),
    }

