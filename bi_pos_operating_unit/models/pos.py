# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_pos_operating_unit(self):
        return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit', default=get_pos_operating_unit, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise ValidationError(_('Configuration error\nThe Company in'
                                        ' the Sales Order and in the Operating'
                                        ' Unit must be the same.'))

    '''@api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['operating_unit_id'] = self.operating_unit_id.id
        return invoice_vals'''
        
        
class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    operating_unit_id = fields.Many2one(related='order_id.operating_unit_id', string='Operating Unit', readonly=True)


class pos_config(models.Model):
    _inherit = 'pos.config'

    @api.model
    def get_pos_operating_unit(self):
        return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit', default=get_pos_operating_unit,)

    @api.constrains('operating_unit_id','stock_location_id')
    def _check_operating_unit_constrains(self):
        if self.operating_unit_id:
            if self.operating_unit_id.id != self.env.user.default_operating_unit_id.id:
                raise UserError(_('Configuration error\nYou  must select the same Operating Unit as On User in point of sale configuration.'))


class pos_session(models.Model):
    _inherit = 'pos.session'

    @api.model
    def create(self,vals):
        res = super(pos_session, self).create(vals)
        res.operating_unit_id = res.config_id.operating_unit_id.id
        return res

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')
