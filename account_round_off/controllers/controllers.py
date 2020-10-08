# -*- coding: utf-8 -*-
# from odoo import http


# class AccountRoundOff(http.Controller):
#     @http.route('/account_round_off/account_round_off/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_round_off/account_round_off/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_round_off.listing', {
#             'root': '/account_round_off/account_round_off',
#             'objects': http.request.env['account_round_off.account_round_off'].search([]),
#         })

#     @http.route('/account_round_off/account_round_off/objects/<model("account_round_off.account_round_off"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_round_off.object', {
#             'object': obj
#         })
