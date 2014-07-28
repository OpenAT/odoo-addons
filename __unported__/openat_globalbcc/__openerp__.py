# -*- coding: utf-8 -*-
##############################################################################
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
    'name': "OpenAT Global BCC",
    'version': "1.0",
    'category': "Tools",
    'summary': "openat_globalbcc",
    'description': """
		Sämtliche E-Mails die von OpenERP gesendet werden werden mittels bcc an eine Mailadresse weitergeleitet.

		Die Mailadresse für die Weiterleitung kann dabei pro Modell (z.B.: project.task) festgelegt werden.
    """,
    'author': "OpenAT und Camadeus",
    'website': "http://www.OpenAT.at",
	'css': [],
    'images': [],
    'depends': ['base','mail'],
    'update_xml':['openat_globalbcc_view.xml',
                  'security/ir.model.access.csv'
                  ],
    'data': [],
    'demo': [],
    'test': [],
    'installable': False,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
