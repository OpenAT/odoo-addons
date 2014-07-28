# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Chatter Improvements',
    'version': '1.0',
    'category': 'Custom',
    'description': """
Chatter Improvements 
===========================
* Followers are displayed in different colors depending on their email notification settings: red if "None", orange: if "Only Incoming"
* New field "Do not add as Follower automatically" which prevents the auto-subscription if a message is sent  (Make sure that internal users have not set this flag)
* Add a new line "Mail sent to" in mail message where all partners are shown which have been successfully notified by e-mail
* When new partners are added in the message compose form, then a warning is shown if the partners will not be notified per e-mail

    """,
    'author': 'camadeus Consulting GmbH',
    'website': 'http://www.camadeus.at',
    'depends': ['web','mail','base'], 
    'js': [
        'static/src/js/chatter_improvements.js',
    ],
    'css': [
        'static/src/css/chatter_improvements.css',
    ],
    'qweb' : [
        'static/src/xml/*.xml',
    ],    
    'update_xml': ['chatter_improvements_view.xml',
                   ],
    'demo_xml': [],
    'installable': False,
    'active': False,
}
