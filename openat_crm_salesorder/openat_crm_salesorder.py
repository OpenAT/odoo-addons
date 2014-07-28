# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from tools.translate import _

class openat_crm_salesorder(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def calculate_sum(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        percentage = 0    
        sum = {}
        values = self.browse(cr,uid,ids,context)
        for data in values:
            percentage = data.openat_saleorder_chance
            amount = data.amount_untaxed
            revenue = 0.0
            temp_rev = amount * percentage
            if temp_rev is not 0.0 or temp_rev is not None: 
                revenue = temp_rev / 100
            sum[data.id] = {'openat_saleorder_revenue' : revenue}
        return sum
    
    """
        Function checks if the entered value is between 0 and 100 as this represents a percentage value to calculate the possible income.
    """
    def _check_percentage(self, cr, uid, ids, context=None):
        if context is None:
            context = {} 
        for data in self.browse(cr, uid, ids, context):
            if data.openat_saleorder_chance < 0 or data.openat_saleorder_chance > 100:
                return False
        return True
    
    _columns = {
                'openat_saleorder_advisor' : fields.many2one('res.partner', 'Sachbearbeiter'),
                'openat_saleorder_chance' : fields.integer('Wahrscheinlichkeit'),
                'openat_saleorder_datedone' : fields.date('Abschluß erwartet bis'),
                'openat_saleorder_revenue' : fields.function(calculate_sum, method=True, multi='revenue', string='CRM Summe'),
    }
        
    """
		The ceck_percentage constraint calls the function _check_percentage each time the save-button was pressed by the user
    """
    _constraints = [(_check_percentage, 'Fehler: Nur Werte zwischen 0 und 100 erlaubt!', ['openat_saleorder_chance'])]
	
openat_crm_salesorder()