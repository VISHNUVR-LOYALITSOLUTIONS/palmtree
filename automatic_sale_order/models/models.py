# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Saleorder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def auto_sale_order(self):

        sale_orders = self.search([('state','=','draft')],limit=5)

        for order in sale_orders:
            order.action_confirm()

