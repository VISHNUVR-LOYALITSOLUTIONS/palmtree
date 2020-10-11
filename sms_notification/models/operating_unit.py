# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    sms_template_id = fields.Many2many('sms.template',string="SMS Template")