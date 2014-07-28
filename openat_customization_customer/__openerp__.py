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
    'name': "OpenAT Kundenanpassungen",
    'version': "1.0",
    'category': "Tools",
    'summary': "openat_customization_customer",
    'description': """
Alle zusätzlichen Felder und Anpassungen die speziell für diesen Kunden angepasst oder erstellt werden.

Dieses Modul wird sinvoller weise natürlich nicht upgedated ;)
		
ACHTUNG: Wenn Anpassungen für Felder oder Ansichten von anderen Modulen vorgenommen werden muss vor allem darauf
geachtet werden dass hier alle diese Module bei den Abhängigkeiten eingetragen werden!
    """,
    'author': "OpenAT",
    'website': "http://www.OpenAT.at",
	'css' : ['static/src/css/style.css'],
    'images': [],
    'depends': ['base'],
    'data': ['openat_customization_customer_view.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
