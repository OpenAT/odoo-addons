# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
from openerp.osv.orm import except_orm
from openerp import pooler
from openerp.osv.osv import except_osv
from openerp import SUPERUSER_ID

class openat_globalbcc(osv.Model):
    _name='mail.bcc'
    _description='Email BCC Config'
    _order='openat_model_id,openat_sequence'
    _rec_name='openat_mail_bcc'
    
    _columns = {
                'openat_model_id': fields.many2one('ir.model','Model',help=_('Specify the name of the model to apply BCC.\nLeave this empty if you want to apply it to all sent emails.')),
                'openat_mail_bcc': fields.char('BCC Mail Address', required=True, size=128, help=_('This address is added to the BCC list of every sent email.')),
                'openat_sequence': fields.integer('Sequence',required=True,help=_('Sequence is used for ordering. If there exist more than one record for specific model, the one with the lowest sequence is chosen.'))
                }
openat_globalbcc()

class openat_globalbcc_ir_mail_server(osv.Model):
    _inherit='ir.mail_server'
    
    '''
    Hook for mail.bcc config:
    Find a suitable bcc config and inject it to the email bcc!
    '''
    def build_email(self, email_from, email_to, subject, body, email_cc=None, email_bcc=None, reply_to=False,
               attachments=None, message_id=None, references=None, object_id=False, subtype='plain', headers=None,
               body_alternative=None, subtype_alternative='plain'):
        if email_bcc is None:
            email_bcc=[]
            
        bcc_obj = self.pool.get('mail.bcc')  
         
        model=False
        bcc_ids = []
        
        cr = pooler.get_db(self.pool.db.dbname).cursor()
        #object_id: e.g.: 47-res.partner
        if object_id and '-' in object_id:
            id,model = object_id.split('-')
        
        if model:
            #search for specific model
            bcc_ids = bcc_obj.search(cr,SUPERUSER_ID,[('openat_model_id','=',model)],limit=1)
            
        if not len(bcc_ids):
            #either no model specified or no model found -> search for global bcc
            bcc_ids = bcc_obj.search(cr,SUPERUSER_ID,[('openat_model_id','=',False)],limit=1)  
        
        #write bcc
        bcc_data = bcc_obj.browse(cr,SUPERUSER_ID,bcc_ids)
        if bcc_data and bcc_data[0]:
            email_bcc.append(bcc_data[0].openat_mail_bcc)
        
        cr.close()
            
        res = super(openat_globalbcc_ir_mail_server,self).build_email(email_from, email_to, subject, body, email_cc=email_cc, email_bcc=email_bcc, reply_to=reply_to,
               attachments=attachments, message_id=message_id, references=references, object_id=object_id, subtype=subtype, headers=headers,
               body_alternative=body_alternative, subtype_alternative=subtype_alternative)
        
        return res
    
openat_globalbcc_ir_mail_server()