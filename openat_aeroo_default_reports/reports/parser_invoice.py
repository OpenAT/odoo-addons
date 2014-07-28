# -*- encoding: utf-8 -*-

from report import report_sxw

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.context = context
        self.localcontext.update({
                                    'get_subtotal': self._get_subtotal,
                                    })
    
    def _get_subtotal(self, subtotal):
        invoice = subtotal.invoice_id
        subtotal_id = subtotal.id
        invoice_lines = invoice.invoice_line
        if not invoice_lines:
            return 0
        sub_total = 0
        for cur_line in invoice_lines:
            if cur_line.product_id.name=='SUBTOTAL' and cur_line.id == subtotal_id:
                return sub_total
            elif cur_line.product_id.name == 'SUBTOTAL' and cur_line.id != subtotal_id:
                sub_total = 0
            elif cur_line.product_id.name == 'HEADER':
                continue
            else:
                sub_total = sub_total + cur_line.price_subtotal
