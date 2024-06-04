# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Real Estate Account',
    'version' : '17.0',
    'summary': 'Real Estate Account Management Software',
    'sequence': -1,
    'description': """Real Estate Account Management Software""",
    'category': 'Real Estate',
    'website': 'https://www.odoo.com',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base', 'real_estate', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/master_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
