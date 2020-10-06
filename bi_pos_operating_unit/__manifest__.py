# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS Operating Unit in Odoo",
    "version" : "13.0.0.1",
    "category" : "Point of Sale",
    "depends" : ['base','sale','point_of_sale','operating_unit'], #,'account_operating_unit'
    "author": "BrowseInfo",
    'summary': 'Apps for Multiple Operating Unit on POS multi operation unit pos multi branch pos multiple branch on point of sales multi branch multi operating unit on point of sales operating unit on pos unit operation management',
    "description": """
       POS Multiple operating unit management for single company, Multiple pos operation management for single company, POS multiple operation for single company.
     multiple Branch for POS
     multiple operating unit for POS,
    multiple unit on POS
    multiple unit operation for POS
    branch on POS session
    Branch on POS receipt
    different unit on POS
    POS Unit Operation For single company
    operating unit on POS session
    operating unit on POS receipt
    different unit operation on POS
    POS multiple Unit Operation For single company
    
    """,
    "website" : "https://www.browseinfo.in",
    "price": 29,
    "currency": "EUR",
    "data": [
        'views/custom_pos_view.xml',
        'security/point_of_sale_security.xml',
    ],
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url": "https://youtu.be/aoQnN3d52xc",
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
