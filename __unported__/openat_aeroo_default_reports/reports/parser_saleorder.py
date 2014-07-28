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
        sale_order = subtotal.order_id
        subtotal_id = subtotal.id
        whattodo = subtotal.product_id.name
        order_lines = sale_order.order_line
        if not order_lines:
            return 0
        sub_total = 0.0
        for cur_line in order_lines:
            # if the line the subtotal is requested for is current
            if cur_line.product_id.name in ['SUBTOTAL', 'SUBTOTAL-ALL'] and cur_line.id == subtotal_id:
                return sub_total
            # if the line is subtotal line but not the one requested
            elif cur_line.product_id.name in ['SUBTOTAL', 'SUBTOTAL-ALL'] and cur_line.id != subtotal_id:
                sub_total = 0
            elif cur_line.product_id.name == 'HEADER':
                continue
            elif whattodo == 'SUBTOTAL':
                if not getattr(cur_line, "hide_subtotal", False):
                    sub_total = sub_total + cur_line.price_subtotal
                else:
                    continue
            elif whattodo == 'SUBTOTAL-ALL':
                sub_total = sub_total + cur_line.price_subtotal
        return sub_total