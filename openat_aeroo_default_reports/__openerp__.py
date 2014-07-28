# -*- encoding: utf-8 -*-

{
    "name" : "OpenAT Aeroo Default Reports",
    "version" : "1.1",
    "description" : """

This Module adds a default aeroo report for
===========================================
* Sales Order (Quotations)
* Purchase Order
* Invoice - OUT
* Delivery Order - OUT

It also adds a default Stylesheet that can be used by all reports e.g. for a global company template.

Workflow
========
If you want to change / customize your reports you should download them and then change then from file based template to
database based template before you upload your changed .odt or .ods file(s).

With this workflow you can always change back to file based template to get the original report in case something
happened.

The Reports are all based on Aeroo Reports - you will find more information on how to change or edit them on the
Alistek Webpage!


ATTENTION
=========
This set of reports will only work with aeroo_report and the module openat_aeroo_reports_extensions

    """,
    "author" : "OpenAT and Alistek Ltd.",
    "website" : "http://www.openat.at",
    "url" : "http://www.openat.at",
    "depends" : ['base', 'report_aeroo', 'sale', 'account', 'portal_sale', 'delivery', 'purchase', 'openat_aeroo_reports_extensions'],
    "init_xml" : [],
    "update_xml" : ['reports/custom_reports.xml',
                    'data/custom_reports_data.xml',
                    'preprocess.xml',
                    'custom_reports_view.xml'],
    "demo_xml" : [],
    "installable" : True,
    "active" : False,
}
