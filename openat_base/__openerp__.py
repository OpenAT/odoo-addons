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
    'name': "OpenAT Base",
    'version': "1.2",
    'category': "Tools",
    'summary': "openat_base",
    'description': """
Alle CSS-Basisanpassungen werden mit diesem Modul vorgenommen.

Es installiert weiters alle Addons die wir für eine Standardinstallation von einer OpenAT OpenERP Instanz benötigen.

EXPORTSCRIPT:
Weiters findet sich in dem Ordner des Addons ein Beispiel-Python-Script für den Export von Berichten mit XMLRPC
    """,
    'author': "OpenAT",
    'website': "http://www.OpenAT.at",
	'css': ['static/src/css/style.css'],
    'images': [],
    'depends': [
        'base', 'crm', 'mail',
        'contacts', 'project', 'sale', 'account_voucher', 'point_of_sale', 'project', 'project_issue', 'note',
        'account_accountant', 'sale', 'stock', 'mrp', 'purchase', 'hr', 'hr_timesheet_sheet', 'hr_recruitment',
        'hr_holidays', 'hr_expense', 'hr_evaluation', 'contacts', 'base_calendar', 'event', 'fleet',
        'account_cancel', 'analytic',
        'cam_hr_overtime', 'chatterimprovements', 'cron_run_manually', 'disable_openerp_online',
        'google_map_and_journey', 'mail_organizer', 'mass_editing', 'openat_aeroo_default_reports',
        'openat_customization_customer', 'openat_globalbcc',
        'openat_partner_fullhierarchy', 'openat_project_advancedviews', 'openat_timetracking_setcharge',
        'partner_history', 'project_description', 'project_task_work_calendar_view',
        'report_aeroo', 'report_aeroo_ooo', 'report_aeroo_printscreen', 'openat_aeroo_reports_extensions',
        'web_ckeditor4', 'web_export_view', 'web_filter_tabs', 'web_group_expand',
        'web_mail_img', 'web_popup_large', 'web_widget_float_formula'
        ],
    'data': [
        'openat_base_view.xml',
        'openat_base_data.xml'
        ],
    'update_xml': [
        'res_config_view.xml'
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
