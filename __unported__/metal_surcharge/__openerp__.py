{
    'name': 'Metal Surcharge Addons',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Binary Quest Limited',
    'website': 'www.binaryquest.com',
    'description': '''
    This Module is for add surcharge for metal product.
    For sales orders it should be possible to attach a metal surcharge based on the German Metal Prices (=DEL). The surchrage is automatically updated weekly and must not influence the sale order line's discount. The amount of the surcharge must also be visible/transfered to all documents that follow a sale order e.g. invoices.
    ''',
    'depends': ['sale', 'mail'],
    'data': ['surcharge_type_view.xml', 'product_view.xml', 'sale_view.xml', 'update_surcharge.xml'],
    'installable': False,
}
