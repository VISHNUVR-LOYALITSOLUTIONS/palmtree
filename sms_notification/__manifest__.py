# -*- coding: utf-8 -*-
{
    'name': "sms_notification",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management', 'stock','sms','operating_unit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/operating_unit.xml',
        'views/templates.xml',
        'security/ir_rule.xml',
        'wizard/sms_template_preview_view.xml',
        'edi/general_messages.xml',
        'edi/sms_template_for_order_creation.xml',
        'edi/sms_template_for_order_confirm.xml',
        'edi/sms_template_for_invoice_validate.xml',
        'edi/sms_template_for_delivery_done.xml',
        'edi/sms_template_for_invoice_payment_register.xml',
        'views/configure_gateway_view.xml',
        'views/sms_sms_view.xml',
        'views/sms_group_view.xml',
        'views/res_config_view.xml',
        'views/sms_report_view.xml',
        'views/sms_cron_view.xml',
        'views/sms_template_view.xml',
        'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
