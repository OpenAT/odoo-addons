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

import logging

from openerp.osv import osv, fields
from openerp.tools.translate import _
import base64
from openerp import netsvc

_logger = logging.getLogger(__name__)

# By Mike: Export of the reports with function print_report from Andreas Brueckl
class ir_cron(osv.osv):
    _name = 'ir.cron'
    _inherit = 'ir.cron'

    def openat_print_report(self, cr, uid, ids, report, outfilename, context=None):
        data = {}
        data['model'] = context['model']
        obj = netsvc.LocalService(report)
        (result, format) = obj.create(cr, uid, ids, data, context)
        outfile = open(outfilename, 'wb')
        #base64.decodestring(result))
        outfile.write(result)
        outfile.close()
        return True


class openat_base(osv.osv):
    _name = "openat_base"

openat_base()


class openat_base_configuration(osv.osv_memory):
    _name = 'openat.base.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'module_openat_aeroo_default_reports': fields.boolean('Openat Aeroo Reports for sale, purchase, warehouse and invoice',
            help = """Replaces the original rml reports with OpenAT Areoo Reports
            It installs the openat_aeroo_default_reports."""),
    }

openat_base_configuration() 
