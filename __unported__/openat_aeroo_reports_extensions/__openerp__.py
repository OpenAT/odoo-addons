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
{
    "name" : "OpenAT Aeroo Report Extensions",
    "version" : "1.2",
    "description" : """
This Module adds the possibility to add optional Products, Headers and Subtotals to Sales Orders and Invoices.

New Functions for Sales-Order-Lines
========================================
* Hide the price on the report-line -> H
* Exclude from Subtotal -> ES
* Exclude from Grand-Total of the sales Order -> ET
* Add a Product called SUBTOTAL and you will get a Subtotal on the report (from this line to the last Subtotal)
* Add a Product called SUBTOTAL-ALL and you will get a Subtotal including all lines on the report
* Add a Product called HEADER and this will be printed as a Header on the report.

New Functions for Sales-Orders and Invoices
========================================
* Include Image: The Product Images will be printed Reports
* Include Description: The Long Description of Products will be printed on Reports

If you confirm a Sales Order no SO-Line with "Exclude from Grand-Total" is allowed since this would make no
sence for the generated Invoices.

ATTENTION: You will have to write custom aeroo-reports for sales orders and invoices
    """,
    "author" : "OpenAT and Alistek Ltd.",
    "website" : "http://www.openat.at",
    "url" : "http://www.openat.at",
    'depends' : ['base', 'sale', 'account', 'report_aeroo'],
    "init_xml" : [],
    'update_xml' : ["openat_aeroo_reports_extensions.xml"],
    "demo_xml" : [],
    'installable': False,
    'active': False,
    'application': False,
}
