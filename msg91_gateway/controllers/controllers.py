# -*- coding: utf-8 -*-
# from odoo import http


# class Msg91Gateway(http.Controller):
#     @http.route('/msg91_gateway/msg91_gateway/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/msg91_gateway/msg91_gateway/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('msg91_gateway.listing', {
#             'root': '/msg91_gateway/msg91_gateway',
#             'objects': http.request.env['msg91_gateway.msg91_gateway'].search([]),
#         })

#     @http.route('/msg91_gateway/msg91_gateway/objects/<model("msg91_gateway.msg91_gateway"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('msg91_gateway.object', {
#             'object': obj
#         })
