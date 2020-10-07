# -*- coding: utf-8 -*-
# from odoo import http


# class Gstr2AccountReport(http.Controller):
#     @http.route('/gstr2_account_report/gstr2_account_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gstr2_account_report/gstr2_account_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gstr2_account_report.listing', {
#             'root': '/gstr2_account_report/gstr2_account_report',
#             'objects': http.request.env['gstr2_account_report.gstr2_account_report'].search([]),
#         })

#     @http.route('/gstr2_account_report/gstr2_account_report/objects/<model("gstr2_account_report.gstr2_account_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gstr2_account_report.object', {
#             'object': obj
#         })
