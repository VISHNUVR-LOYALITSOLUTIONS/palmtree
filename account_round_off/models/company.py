# -*- coding: utf-8 -*-

from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo import fields, models, api, _

class RoundOffSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    round_off = fields.Boolean(string='Allow rounding of invoice amount', help="Allow rounding of invoice amount")
    # sale_round_off_account = fields.Many2one('account.account', string='Sale Round Off Account',)
    round_off_account = fields.Many2one('account.account', string="Purchase Round Off Account")

    def set_values(self):
        res = super(RoundOffSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account_round_off.round_off', self.round_off)
        self.env['ir.config_parameter'].sudo().set_param('account_round_off.round_off_account', self.round_off_account.id)

        return res


    # def set_round_off(self):
    #     ir_values_obj = self.env['ir.values']
    #     ir_values_obj.sudo().set_default('resfig.settings', "round_off", self.round_off)
    #     ir_values_obj.sudo().set_default('res.config.settings', "round_off_account", self.round_off_account.id)



    @api.model
    def get_values(self):
        res = super(RoundOffSetting, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['round_off'] = (get_param('account_round_off.round_off'))
        res['round_off_account'] = int(get_param('account_round_off.round_off_account'))

        return res

    # @api.model
    # def get_values(self):
    #     res = super(RoundOffSetting, self).get_values()
    #     res.update(
    #         round_off=self.env['ir.config_parameter'].sudo().get_param(
    #             'account_round_off.round_off'),
    #         round_off_account=self.env['ir.config_parameter'].sudo().get_param(
    #             'account_round_off.round_off_account'),
    #     )
    #     return res
    # 
    # my_custom_field1_id = int(
    #     self.env['ir.config_parameter'].sudo().get_param('your_custom_module_name.my_custom_field1_id')),

    # def set_values(self):
    #     super(RoundOffSetting, self).set_values()
    #     param = self.env['ir.config_parameter'].sudo()
    #
    #     round_off = self.round_off or False
    #     round_off_account = self.round_off_account and self.round_off_account.id or False
    #
    #     param.set_param('account_round_off.round_off', round_off)
    #     param.set_param('account_round_off.round_off_account', round_off_account)