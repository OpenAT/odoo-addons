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

import os
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime
from openerp.osv import osv, fields


class product_metal_surcharge_type(osv.osv):
    _inherit = 'product.metal.surcharge.type'

    def _run_scheduler(self, cr, uid, context=None):
        ''' Runs through scheduler.
        '''
        #print "_run_scheduler"
        
        context = context or {}
        rate_obj = self.pool.get('metal.surcharge.rate')
        surcharge_types = self.search(cr, uid, [('source_url', '!=', None)])
        surcharge_types = self.browse(cr, uid, surcharge_types)
        for sur_obj in surcharge_types:
            f = urllib.urlopen(sur_obj.source_url)
            html = f.read()
            #soup = BeautifulSoup(''.join(html))
            soup = BeautifulSoup(html)
            #print(soup.prettify())
            
            # Find all the tables using BeautifulSoup Methods
            tables = soup.findChildren('table')
            
            # This will get the first table. Your page may have more.
            my_table = tables[0]
            
            # This will give you all the Rows of your first table:
            rows = my_table.findChildren(['tr'])
            #Getting the Second Row (for my case this row was needed).
            my_row = rows[1]
            
            #Getting Column of this row
            cells = my_row.findChildren('td')
            
            cellDate = cells[0]
            cellData = cells[1]
            
            value = cellData.string.replace(",", "")
            #print value
            dt = datetime.strptime(cellDate.string,'%d. %B %Y')
            
            #print sur_obj.rate_ids
            #if (sur_obj.rate_ids):
            #    dbdt = datetime.strptime(sur_obj.last_update,'%Y-%m-%d %H:%M:%S')
            #else:
            #    print "_run_scheduler"
            #    print datetime.strptime('2013-01-01 00:00:01','%Y-%m-%d %H:%M:%S')
            #    #dbdt = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
            
            #if (dbdt.date()<dt.date()):
            vals = {
                    'name': dt,
                    'rate': value,
                    'surcharge_type_id': sur_obj.id,
                    }
            rate_obj.create(cr, uid, vals, context=context)            
            

product_metal_surcharge_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
