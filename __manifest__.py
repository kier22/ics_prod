# -*- coding: utf-8 -*-
{
    'name': "ICS Module",

    'summary': """
        ICS's Custom models which apply required changes to native and other custom models """,

    'description': """
        TODO ADD RELEASE NOTES
    """,

    'author': "Kieran Leabon",
    'website': "",

    #
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mail', 'contract', 'contract', 'l10n_uk',
                'crm', 'sale_management', 'project', 'base_automation'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/ics_groups.xml',
        # 'wizards/crm_quotation_partner.xml',
        'reports/invoices.xml',
        'reports/quotes.xml',
        'views/contract.xml',
        'views/crm_lead.xml',
        # 'views/sales_logic.xml',
        'views/templates.xml',
        'views/products.xml',
        'views/portal.xml',
        'views/quick_opp_create.xml',
        'views/portal_template.xml',
        'views/partner.xml',
        # 'views/crm_quotation_partner.xml',
        # 'views/contract_portal.xml',
        'views/sales.xml',
        'views/day_tag.xml',
        #'views/sale_due_remainder_view.xml',
        'data/sequence.xml',
        # added email template xml
        'data/mail_template_data.xml',
    ]}
