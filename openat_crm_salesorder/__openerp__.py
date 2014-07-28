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

{
    'name': "OpenAT CRM für Angebote",
    'version': "1.0",
    'category': "Tools",
    'summary': "openat_crm_salesorder",
    'description': """
		Durch dieses Modul können bei Angeboten (Sale.Order) zusätzlich eine Wahrscheinlichkeit des Abschlusses in %, sowie ein erwartetes Abschlussdatum und ein Sachbearbeiter eingetragen werden. Es rechnet dann automatisch eine wahrscheinliche Angebotssumme über die Formel "Wahrscheinlichkeit des Abschlusses in %" * Abgebotssumme = Forecast
		
		Zusätzlich kann die Angebotsliste nach Monat gruppiert werden um eine Auswertung über die erwartetete Abschlusssumme in einem Monat zu erhalten.
    """,
    'author': "OpenAT",
    'website': "http://www.OpenAT.at",
    'images': [],
    'depends': ['base', 'sale'],
    'data': ['openat_crm_salesorder_view.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
