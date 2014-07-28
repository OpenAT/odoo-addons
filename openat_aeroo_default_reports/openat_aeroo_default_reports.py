# -*- encoding: utf-8 -*-

from openerp.osv import osv,fields
from openerp.tools.translate import _

class ir_actions_report_xml(osv.osv):
    _name = 'ir.actions.report.xml'
    _inherit = 'ir.actions.report.xml'

    def _remake_print_button(self, cr, uid, src_id, dest_id):
        ir_values_obj = self.pool.get('ir.values')
        event_id = ir_values_obj.search(cr, uid, \
                [('value','=',"ir.actions.report.xml,%s" % src_id)])
        if event_id:
            ir_values_obj.write(cr, uid, event_id[0], \
                    {'value':"ir.actions.report.xml,%s" % dest_id})
        
        return True

    _columns = {
    }

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def do_button_print(self, cr, uid, ids, context=None):
        res = super(res_partner, self).do_button_print(cr, uid, ids, context=context)
        res['report_name'] = 'account_followup.followup.print.openat'
        return res

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    def invoice_print(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).invoice_print(cr, uid, ids, context=context)
        res['report_name'] = 'account.invoice.openat'
        return res

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def print_quotation(self, cr, uid, ids, context=None):
        res = super(sale_order, self).print_quotation(cr, uid, ids, context=context)
        res['report_name'] = 'sale.order.openat'
        return res

class purchase_order(osv.osv):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    def print_quotation(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).print_quotation(cr, uid, ids, context=context)
        res['report_name'] = 'purchase.order.openat'
        return res

