# -*- coding: utf-8 -*-
# #############################################################################
#
# OpenAT
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

import datetime

from osv import osv, fields
from openerp import tools
from openerp.tools.translate import _


class product_template(osv.Model):
    # Ist mir noch unklar wie die Inheritance hier funktioniert - des is scho speziell - denke aber das es sich hier
    # um eine art super init handelt das in osv.Model stattfindet?!? - to be found
    _inherit = 'product.template'

    def __init__(self, cr, uid):
        # Super ist mir noch suspekt die frage ist ob man das auch so schreiben koennte
        # dieser schritt bedeutet meiner Meinung nach nix anderes als das eben in unserem erweiterten init zuerst der
        # __init__ originalen Klasse ausgefuehrt wird.
        super(product_template, self).__init__(cr, uid)

        # Versuch 1 Fuehrt leider zu recursion ?!?
        # Wahrscheinlich da die beiden klassen den selben namen haben also es sich eben nicht um eine ableitung
        # der originalen klasse handelt sondern eben um ein ueberschreiben
        #product_template.__init__(self, cr, uid)

        # Nach dem init der Originalen Klasse ueberschreiben wir gleich ein paar seiner attribute - im speziellen
        # den inhalt des state wertes des dictionaries _columns. Da der Wert von state wiederum ein eigenes objekt ist
        # naemlich ein fields.selection Objekt muessen wir auf dieses wie folgt zugreifen
        # fields.selection.selection -> das bedeutet also _columns['state'].selection
        # da in _columns['state'] das Objekt fields.selection "zugewiesen" ist
        # das objekt fields.selection hat ein attribut namens selection in dem die selection list enthalten ist
        # Deshalb kommt da auch eine Liste zurück und nicht das objekt ;)

        # leere Elemente loeschen
        self._columns['state'].selection = [x for x in self._columns['state'].selection if x != ('', '')]

        # neue Elemente anhaengen
        for newstate in [('ppnew', 'New'), ('pptocheck', 'To Check'), ('ppapproved', 'Approved')]:
            if newstate not in self._columns['state'].selection:
                self._columns['state'].selection.append(newstate)


product_template()


class product_product(osv.Model):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        'openat_csp_nummer': fields.char('CSP Article ID', size=64, required=True, translate=False, readonly=True,
                                         states={'ppnew': [('required', False), ('readonly', False)]}),
        'openat_bezeichnung': fields.char('Article Name', translate=True),
        # Markennamen sollen als Tags geloest werden
        'openat_markenname_ids': fields.many2many('openat_produktpass.markenname', string='Brand Names'),
        # Warengruppe = Produktgruppe - To Be Tested
        # Warenuntergruppe wird ebenfalls ueber Produktgruppe geregelt - To Be Tested
        'openat_verkehrsbezeichnung': fields.char('Trading Name', translate=True),
        # Produktfoto - Feld Bereits vorhanden
        'openat_ean_verkauf': fields.char('EAN-CODE Unit of Sale', translate=False),
        'openat_ean_bestell': fields.char('EAN-CODE Order Unit', translate=False),
        # nicht mehr notwendig: ersetzt durch weight_net
        #'openat_nettofuellgewicht': fields.integer('Net Fill Weight (g)'),
        'openat_referenzprodukte': fields.text('Reference Products', translate=True),
        #'openat_produktionsstaette': fields.text('Production Facility', translate=True),
        'openat_produktionsstaette': fields.many2one('res.partner', 'Production Facility'),
        # Lager und Transport Anweisung
        'openat_lagerundtransport_id': fields.many2one('openat_produktpass.lagerundtransport',
                                                       'Storage / Transport Instructions'),
        'openat_temperatur': fields.related('openat_lagerundtransport_id', 'openat_temperatur',
                                            type='integer', relation='openat_produktpass.lagerundtransport',
                                            string="Temperature", readonly="1"),
        'openat_luftfeuchte': fields.related('openat_lagerundtransport_id', 'openat_luftfeuchte',
                                             type='integer', relation='openat_produktpass.lagerundtransport',
                                             string="Humidity", readonly="1"),
        'openat_licht': fields.related('openat_lagerundtransport_id', 'openat_licht',
                                       type='text', relation='openat_produktpass.lagerundtransport',
                                       string="Lighting Conditions", readonly="1"),
        'openat_lageranweisung': fields.related('openat_lagerundtransport_id', 'openat_lageranweisung',
                                                type='text', relation='openat_produktpass.lagerundtransport',
                                                string="Storage Instructions", readonly="1"),
        'openat_lieferanweisung': fields.related('openat_lagerundtransport_id', 'openat_lieferanweisung',
                                                 type='text', relation='openat_produktpass.lagerundtransport',
                                                 string="Transport Instructions", readonly="1"),
        'openat_lt_beschreibung': fields.related('openat_lagerundtransport_id', 'openat_licht',
                                                 type='text', relation='openat_produktpass.lagerundtransport',
                                                 string="Storage and Transport Method Description", readonly="1"),
        # Konservierungsmethode
        'openat_konservierungsmethode_id': fields.many2one('openat_produktpass.konservierungsmethode',
                                                           'Preservation Method'),
        'openat_temp': fields.related('openat_konservierungsmethode_id', 'openat_temp',
                                      type='integer', relation='openat_produktpass.konservierungsmethode',
                                      string="Temperature (°C)", readonly="1"),
        'openat_zeit': fields.related('openat_konservierungsmethode_id', 'openat_zeit',
                                      type='char', relation='openat_produktpass.konservierungsmethode',
                                      string="Time", readonly="1"),
        'openat_schutzbegasung': fields.related('openat_konservierungsmethode_id', 'openat_schutzbegasung',
                                                type='char', relation='openat_produktpass.konservierungsmethode',
                                                string="Protective Gas", readonly="1"),
        'openat_gaszusammensetzung': fields.related('openat_konservierungsmethode_id', 'openat_gaszusammensetzung',
                                                    type='text', relation='openat_produktpass.konservierungsmethode',
                                                    string="Gas Types", readonly="1"),
        'openat_km_beschreibung': fields.related('openat_konservierungsmethode_id', 'openat_beschreibung',
                                                 type='text', relation='openat_produktpass.konservierungsmethode',
                                                 string="Description", readonly="1"),
        #
        # ersetzt durch life_time
        #'openat_mindesthaltbarkeitsdauer': fields.integer('Expiry (days)'),
        # ersetzt durch use_time
        #'openat_restlaufzeit': fields.integer('Remaining Life (days)'),
        #
        'openat_zutatenliste': fields.text('Ingredients', translate=True),
        # Naehrwerte big 7 pro 100g
        'openat_brennwert_kj': fields.integer('Calorific Value (kJ)*'),
        'openat_brennwert_kcal': fields.integer('Calorific Value (kcal)*'),
        'openat_fett': fields.integer('Fat (g)*'),
        'openat_gesaettigte_fettsauren': fields.integer('Saturated Fatty Acids (g)*'),
        'openat_einfach_ungesaettigte_fettsauren': fields.integer('Monounsaturated Fatty Acids (g)'),
        'openat_mehrfach_ungesaettigte_fettsauren': fields.integer('Polyunsaturated Fatty Acids (g)'),
        'openat_kohlenhydrate': fields.integer('Carbohydrates (g)*'),
        'openat_kohlenhydrate_zucker': fields.integer('Carbohydrates Sugar (g)*'),
        'openat_ballaststoffe': fields.integer('Dietary Fibre (g)'),
        'openat_eiweiss': fields.integer('Protein (g)*'),
        'openat_natrium': fields.integer('Natrium (g)'),
        'openat_salz': fields.integer('Salt (g)*'),
        'openat_be': fields.char('BE', translate=True),
        # Allergene EU (bolean - writeable nur wenn angehakt - onchange)
        'openat_allergene_getreide': fields.boolean('Glutenhaltiges Getreide sowie daraus hergestellte Erzeugnisse'),
        'openat_allergene_getreide_text': fields.text('Glutenhaltiges Getreide sowie daraus hergestellte Erzeugnisse',
                                                      translate=True),
        'openat_allergene_krebstiere': fields.boolean('Krebstiere u. -erzeugnisse'),
        'openat_allergene_krebstiere_text': fields.text('Krebstiere u. -erzeugnisse', translate=True),
        'openat_allergene_weichtiere': fields.boolean('Weichtiere u. -erzeugnisse'),
        'openat_allergene_weichtiere_text': fields.text('Weichtiere u. -erzeugnisse', translate=True),
        'openat_allergene_ei': fields.boolean('Ei u. -erzeugnisse'),
        'openat_allergene_ei_text': fields.text('Ei u. -erzeugnisse', translate=True),
        'openat_allergene_fisch': fields.boolean('Fisch u. - erzeugnisse'),
        'openat_allergene_fisch_text': fields.text('Fisch u. - erzeugnisse', translate=True),
        'openat_allergene_erdnuesse': fields.boolean('Erdnuesse u. -erzeugnisse'),
        'openat_allergene_erdnuesse_text': fields.text('Erdnuesse u. -erzeugnisse', translate=True),
        'openat_allergene_soja': fields.boolean('Soja u. -erzeugnisse'),
        'openat_allergene_soja_text': fields.text('Soja u. -erzeugnisse', translate=True),
        'openat_allergene_milch': fields.boolean('Milch u. -erzeugnisse '),
        'openat_allergene_milch_text': fields.text('Milch u. -erzeugnisse ', translate=True),
        'openat_allergene_schalenf': fields.boolean('Schalenfruechte u. -erzeugnisse'),
        'openat_allergene_schalenf_text': fields.text('Schalenfruechte u. -erzeugnisse', translate=True),
        'openat_allergene_lupine': fields.boolean('Lupine u. -erzeugnisse'),
        'openat_allergene_lupine_text': fields.text('Lupine u. -erzeugnisse', translate=True),
        'openat_allergene_sellerie': fields.boolean('Sellerie u. - erzeugnisse'),
        'openat_allergene_sellerie_text': fields.text('Sellerie u. - erzeugnisse', translate=True),
        'openat_allergene_senf': fields.boolean('Senf u. - erzeugnisse'),
        'openat_allergene_senf_text': fields.text('Senf u. - erzeugnisse', translate=True),
        'openat_allergene_sesam': fields.boolean('Sesamsamen u. -erzeugnisse'),
        'openat_allergene_sesam_text': fields.text('Sesamsamen u. -erzeugnisse', translate=True),
        'openat_allergene_so2_sulfite': fields.boolean('SO2 u. Sulfite [c > 10 mg/kg od. 10 mg/L as SO2]'),
        'openat_allergene_so2_sulfite_text': fields.text('SO2 u. Sulfite [c > 10 mg/kg od. 10 mg/L as SO2]', translate=True),
        # Die richtige Kennzeichnung wird ausgwaehlt
        'openat_kennzeichnung_id': fields.many2one('openat_produktpass.kennzeichnung',
                                                   'Austrian Labeling'),
        'openat_auslobungen': fields.text('Additional Labelings', translate=True),
        'openat_rohstoffe': fields.text('Other Ingredients / Details', translate=True),
        # Chemische Analysewerte
        'openat_chem_wasser': fields.integer('Water (% / 100g)'),
        'openat_chem_wasser_kodex': fields.integer('Water (% / 100g): Minimum Value from Kodex'),
        'openat_chem_fett': fields.integer('Fat (% / 100g)'),
        'openat_chem_fett_kodex': fields.integer('Fat (% / 100g): Minimum Value from Kodex'),
        'openat_chem_eiweiss': fields.integer('Protein (% / 100g)'),
        'openat_chem_eiweiss_kodex': fields.integer('Protein (% / 100g): Minimum Value from Kodex'),
        'openat_chem_kohlenhydrate': fields.integer('Carbohydrates (% / 100g)'),
        'openat_chem_kohlenhydrate_kodex': fields.integer('Carbohydrates (% / 100g): Minimum Value from Kodex'),
        # Mikrobiologischen Grenzwerte in KBE / g
        # bei Ende MHD Richtwert
        'openat_mikrob_norm_keim': fields.integer('Aer. mes. Gesamtkeimzahl (KBE / g)'),
        'openat_mikrob_norm_clost': fields.integer('mes. sulfitred. Clostridien (KBE / g)'),
        'openat_mikrob_norm_coli': fields.integer('E. Coli (KBE / g)'),
        'openat_mikrob_norm_entero': fields.integer('Enterokokken (KBE / g)'),
        'openat_mikrob_norm_staphy': fields.integer('koag. pos. Staphylokokken (KBE / g)'),
        'openat_mikrob_norm_lacto': fields.integer('Lactobacillen (KBE / g)'),
        'openat_mikrob_norm_cerus': fields.integer('Bacillus cereus (KBE / g)'),
        'openat_mikrob_norm_hefen': fields.integer('Hefen (KBE / g)'),
        'openat_mikrob_norm_schimmel': fields.integer('Schimmel (KBE / g)'),
        'openat_mikrob_norm_salmonellen': fields.integer('Salmonellen (KBE / g)'),
        'openat_mikrob_norm_listeria': fields.integer('Listeria monocytogenes (KBE / g)'),
        'openat_mikrob_norm_ehec': fields.integer('EHEC (KBE / g)'),
        # bei Ende MHD Hoechstwert
        'openat_mikrob_max_keim': fields.integer('Aer. mes. Gesamtkeimzahl (KBE / g)'),
        'openat_mikrob_max_clost': fields.integer('mes. sulfitred. Clostridien (KBE / g)'),
        'openat_mikrob_max_coli': fields.integer('E. Coli (KBE / g)'),
        'openat_mikrob_max_entero': fields.integer('Enterokokken (KBE / g)'),
        'openat_mikrob_max_staphy': fields.integer('koag. pos. Staphylokokken (KBE / g)'),
        'openat_mikrob_max_lacto': fields.integer('Lactobacillen (KBE / g)'),
        'openat_mikrob_max_cerus': fields.integer('Bacillus cereus (KBE / g)'),
        'openat_mikrob_max_hefen': fields.integer('Hefen (KBE / g)'),
        'openat_mikrob_max_schimmel': fields.integer('Schimmel (KBE / g)'),
        'openat_mikrob_max_salmonellen': fields.integer('Salmonellen (KBE / g)'),
        'openat_mikrob_max_listeria': fields.integer('Listeria monocytogenes (KBE / g)'),
        'openat_mikrob_max_ehec': fields.integer('EHEC (KBE / g)'),
        #
        # LOGISTIKTDATEN - die meisten Felder bereits da - muss nur in neue Views gut uebertragen werden ;)
        'openat_tara': fields.integer('Tara (g)'),
        # Zubereitung
        'openat_zubereitungshinweise': fields.text('Cooking', translate=True),
        # Zertifikatsbezeichnung
        'openat_ifs': fields.text('IFS', translate=True),
        # Gensusstauglichkeitskennzeichen
        'openat_genusstauglichkeitskennzeichen': fields.text('Genusstauglichkeitskennzeichen'),
        # DISPLAY
        'openat_display': fields.boolean('Display'),
        'openat_display_ids': fields.one2many('openat_produktpass.display', 'produktpass_id', 'Displaysortierung'),
        #
        # TODO 3 Function Fields
        #
        #'openat_firsimport'
        #'openat_lastimport'
        #'letzteaenderung'
    }
    _defaults = {
        'state': 'ppnew',
    }
    _sql_constraints = [('openat_csp_nummer_unique', 'unique(openat_csp_nummer)', 'CSP Article ID has to be unique!')]


    def check_valid_call(self, cr, uid, ids, context=None):
        productpass = self.read(cr, uid, ids, ['openat_csp_nummer'], context=context)
        if not len(productpass) == 1:
            raise osv.except_osv(
                'None or more than one record found!',
                'Please make sure there is only one Produkt Pass (product.product record) selected'
            )
        if not productpass[0]['openat_csp_nummer']:
            raise osv.except_osv(
                'No CSP Number!',
                'Please assign a valid CSP Number to your Product Pass (product.product.openat_csp_nummer)'
            )
        return True


    def cspnummer_to_external_id(self, cr, uid, ids, context=None, forcecspnumber=0):
        context = context or {}
        print "--------------------------------------------------------"
        print "cspnummer_to_external_id(): START"
        print "--------------------------------------------------------"
        print 'UID: %s' % uid
        print 'IDS: %s' % ids
        print 'Context: %s' % context
        print 'self.read name: %s ' % self.read(cr, uid, ids, ['openat_csp_nummer'])
        #print 'Alle Attribute von product.product: %s' % dir(self)
        #print '---'

        # Read the field openat_csp_nummer for the given ids
        # The Answer is a List with embedded dictionaries of the form [{'id': 5, 'openat_cps_nummer': '123456'}, {...}]
        productpasses = self.read(cr, uid, ids, ['openat_csp_nummer'], context=context)

        # Ensure that there where records found
        if productpasses:
            # Get the object ir.model.data
            irmodeldata = self.pool.get('ir.model.data')

            # Browse through the found productpasses records: pprecord is a dict {'id': 5, 'openat_cps_nummer': '123456'}
            for pprecord in productpasses:
                if pprecord['openat_csp_nummer']:
                    # ToDo: Use Message template with csv record to post message
                    print "Try to post a Message to the Record: %s" % pprecord['id']

                    template_obj = self.pool.get('email.template')
                    template_id = template_obj.search(cr, uid, [('name', '=', 'MikesTemplate')])[0]
                    print 'Email Template ID: %s' % template_id
                    template_obj.send_mail(cr, uid, template_id, pprecord['id'], force_send=False, context=context)

                    # Alte Version ;)
                    #subject = 'Test Message at %s' % (lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    #self.message_post(cr, uid, pprecord['id'], body='Test', subject=subject)

                    # Search for the corresponding ir.model.data record. Answer is an id.
                    irmodeldata_record_id = irmodeldata.search(cr, uid, [('model', '=', 'product.product'),
                                                                         ('res_id', '=', pprecord['id'])])
                    print 'irmodeldata_record_id: %s' % irmodeldata_record_id
                    print 'len(irmodeldata_record_id): %s' % len(irmodeldata_record_id)
                    assert len(
                        irmodeldata_record_id) <= 1, 'More than one record found for ir.model.data: only one allowed'

                    # If a corresponding record already exists update the ir.model.data record with the csp number as name
                    if irmodeldata_record_id:
                        irmodeldata.write(cr, uid, irmodeldata_record_id,
                                          {'name': pprecord['openat_csp_nummer']},
                                          context=context)
                    # If none exists create a new one
                    # ToDo: Check the function export_data and see how it creates the external_id record
                    else:
                        irmodeldata.create(cr, uid,
                                           {'module': '__export__',
                                            'name': pprecord['openat_csp_nummer'],
                                            'model': 'product.product',
                                            'res_id': pprecord['id'], },
                                           context=None)

        print "--------------------------------------------------------"
        print "cspnummer_to_external_id(): STOP"
        print "--------------------------------------------------------"
        return True


    def button_tocheck(self, cr, uid, ids, context=None):
        self.check_valid_call(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state': 'pptocheck'}, context=context)


    def button_approved(self, cr, uid, ids, context=None):
        self.check_valid_call(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state': 'ppapproved'}, context=context)


    # Extend create, write and import_external (=load) functions
    # since these are NOT in the __init__ sections they will only be called on first save of a product.product
    # It may be necessary to move them into __init__ also?
    def create(self, cr, uid, vals, context=None):
        print "create(): Commands BEFORE original method is called"
        return super(product_product, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        print "write(): Commands BEFORE original method is called"
        self.cspnummer_to_external_id(cr, uid, ids, context=context)
        return super(product_product, self).write(cr, uid, ids, vals, context=context)

    def export_data(self, cr, uid, ids, fields_to_export, context=None):
        print "export_data(): Commands BEFORE original method is called"
        return super(product_product, self).export_data(cr, uid, ids, fields_to_export, context=context)

    def load(self, cr, uid, fields, data, context=None):
        print "--------------------------------------------------------"
        print "load(): Commands BEFORE original method is called"
        print "--------------------------------------------------------"
        print "load() fields: %s" % fields
        print "load() data: %s" % data
        # TODO use export_data() to make a full backup of all products and post it as a message to a admin newsgroup
        #
        # TODO Muss noch eine Funktion schreiben die beim Importieren Zeilen ohne gueltige external id = CSP Nummer
        # TODO verweigert. Ausserdem sollten alle Importierten Produkte im Zustand "To Check sein"
        # self.check_valid_import(cr, uid, fields, data, context=context)
        return super(product_product, self).load(cr, uid, fields, data, context=context)


product_product()


class markenname(osv.Model):
    _name = 'openat_produktpass.markenname'
    _columns = {
        'name': fields.char('Brand Name', size=256, required=True, translate=False),
        'produktpass_ids': fields.many2many('product.product', string="Produkt Ids")
    }


markenname()


class lagerundtransport(osv.Model):
    _name = 'openat_produktpass.lagerundtransport'
    _columns = {
        'name': fields.char('Name of Instruction', size=256, required=True, translate=False),
        'openat_temperatur': fields.integer('Temperature'),
        'openat_luftfeuchte': fields.integer('Humidity'),
        'openat_licht': fields.text('Lighting Conditions'),
        'openat_lageranweisung': fields.text('Storage Instructions'),
        'openat_lieferanweisung': fields.text('Transport Instructions'),
        'openat_beschreibung': fields.text('Storage and Transport Method Description'),
    }


lagerundtransport()


class konservierungsmethode(osv.Model):
    _name = 'openat_produktpass.konservierungsmethode'
    _columns = {
        'name': fields.char('Preservation Method (Short Name)', size=256, required=True, translate=False),
        'openat_temp': fields.integer('Preservation Method Temperature (°C)'),
        'openat_zeit': fields.char('Preservation Method Time'),
        'openat_schutzbegasung': fields.char('Preservation Method Protective Gas'),
        'openat_gaszusammensetzung': fields.text('Preservation Method Gas Types'),
        'openat_beschreibung': fields.text('Preservation Method Description'),
    }


konservierungsmethode()


class kennzeichnung(osv.Model):
    _name = 'openat_produktpass.kennzeichnung'
    _columns = {
        'name': fields.char('Name of Instruction', size=256, required=True, translate=True),
        'openat_beschreibung': fields.text('Temperature', required=True, translate=True)
    }


kennzeichnung()


class display(osv.Model):
    _name = 'openat_produktpass.display'
    _columns = {
        'produktpass_id': fields.many2one('product.product', 'Product Pass', ondelete='cascade'),
        'name': fields.char('Art. Nr.', size=256, required=True, translate=True),
        'openat_bezeichnung': fields.text('Description', translate=True),
        'openat_eancode': fields.text('EAN-Code', translate=True)
    }


display()