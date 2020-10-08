# -*- coding: utf-8 -*-
# from odoo import http


# class AutomaticSaleOrder(http.Controller):
#     @http.route('/automatic_sale_order/automatic_sale_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automatic_sale_order/automatic_sale_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('automatic_sale_order.listing', {
#             'root': '/automatic_sale_order/automatic_sale_order',
#             'objects': http.request.env['automatic_sale_order.automatic_sale_order'].search([]),
#         })

#     @http.route('/automatic_sale_order/automatic_sale_order/objects/<model("automatic_sale_order.automatic_sale_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automatic_sale_order.object', {
#             'object': obj
#         })
