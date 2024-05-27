# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Real Estate',
    'version' : '17.0',
    'summary': 'Real Estate Management Software',
    'sequence': -1,
    'description': """Real Estate Management Software""",
    'category': 'Custom',
    'website': 'https://www.odoo.com',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
