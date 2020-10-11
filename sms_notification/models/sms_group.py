# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import models, fields, api, _


class SmsGroup(models.Model):

    _name = "sms.group"
    _description = "This module is used for create the group of customer to send message"

    name = fields.Char(string="Group Name", required=True)
    member_type = fields.Selection([('customer', 'Customer'),
                                    ('supplier', 'Supplier'),
                                    ('any', 'Any')], string="Member Type", default="customer", required=True)
    member_ids = fields.Many2many("res.partner", 'sms_member_group',
                                  column1='member_id', column2='partner_id', string="Members", required=True)
    total_members = fields.Integer(
        compute='get_total_members', string="Total Members", store=True)

    @api.depends("member_ids")
    def get_total_members(self):
        for i in self:
            i.total_members = len(i.member_ids)

    # @api.onchange('member_type')
    # def onchange_member_type(self):
    #     for i in self:
    #         i.member_ids = []
    #         res = {}
    #         if i.member_type == 'customer':
    #             partner = self.env['res.partner'].search([('customer', '=', True)])
    #             res['domain'] = {'member_ids': partner.ids}
    #         if i.member_type == 'supplier':
    #             partner = self.env['res.partner'].search([])
    #             res['domain'] = {'member_ids': partner.ids}
    #         if i.member_type == 'any':
    #             res['domain'] = {'member_ids': []}
    #         return res
