# -*- coding: utf-8 -*-

from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo import fields, models, api, _
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re



# class RoundOffSetting(models.TransientModel):
#     _inherit = 'account.config.settings'
#
#     round_off = fields.Boolean(string='Allow rounding of invoice amount', help="Allow rounding of invoice amount")
#     round_off_account = fields.Many2one('account.account', string='Round Off Account')
#
#     @api.multi
#     def set_round_off(self):
#         ir_values_obj = self.env['ir.values']
#         ir_values_obj.sudo().set_default('account.config.settings', "round_off", self.round_off)
#         ir_values_obj.sudo().set_default('account.config.settings', "round_off_account", self.round_off_account.id)
#

class AccountRoundOff(models.Model):
    _inherit = 'account.move'

    round_off_value = fields.Float(compute='_compute_amount', string='Round off amount')
    rounded_total = fields.Float(compute='_compute_amount', string='Rounded Total')
    round_active = fields.Boolean(compute='get_round_active')
    round_account_id = fields.Integer(compute='get_round_active')
    # purchase_round_account_id = fields.Integer(compute='get_round_active')

    #
    # @api.depends('company_id.round_off')
    def get_round_active(self):
        for rec in self:
            rec.round_active = self.env['ir.config_parameter'].sudo().get_param('account_round_off.round_off') or False
            rec.round_account_id = self.env['ir.config_parameter'].sudo().get_param('account_round_off.round_off_account') or False
            # rec.round_active = rec.company_id.round_off
            # rec.round_account_id = rec.company_id.round_off_account.id

    # 1. tax_line_ids is replaced with tax_line_id. 2. api.mulit is also removed.


    # @api.depends('debit', 'credit', 'account_id', 'amount_currency', 'currency_id', 'matched_debit_ids',
    #              'matched_credit_ids', 'matched_debit_ids.amount', 'matched_credit_ids.amount', 'move_id.state',
    #              'company_id')
    # def _amount_residual(self):
    #     super(AccountRoundOff, self)._amount_residual()
    #
    #     for line in self:
    #         if not line.account_id.reconcile and line.account_id.internal_type != 'liquidity':
    #             line.reconciled = False
    #             line.amount_residual = 0
    #             line.amount_residual_currency = 0
    #             continue
    #         #amounts in the partial reconcile table aren't signed, so we need to use abs()
    #         amount = abs(line.debit - line.credit)
    #         amount_residual_currency = abs(line.amount_currency) or 0.0
    #         sign = 1 if (line.debit - line.credit) > 0 else -1
    #         if not line.debit and not line.credit and line.amount_currency and line.currency_id:
    #             #residual for exchange rate entries
    #             sign = 1 if float_compare(line.amount_currency, 0, precision_rounding=line.currency_id.rounding) == 1 else -1
    #
    #         for partial_line in (line.matched_debit_ids + line.matched_credit_ids):
    #             # If line is a credit (sign = -1) we:
    #             #  - subtract matched_debit_ids (partial_line.credit_move_id == line)
    #             #  - add matched_credit_ids (partial_line.credit_move_id != line)
    #             # If line is a debit (sign = 1), do the opposite.
    #             sign_partial_line = sign if partial_line.credit_move_id == line else (-1 * sign)
    #
    #             amount += sign_partial_line * partial_line.amount
    #             #getting the date of the matched item to compute the amount_residual in currency
    #             if line.currency_id and line.amount_currency:
    #                 if partial_line.currency_id and partial_line.currency_id == line.currency_id:
    #                     amount_residual_currency += sign_partial_line * partial_line.amount_currency
    #                 else:
    #                     if line.balance and line.amount_currency:
    #                         rate = line.amount_currency / line.balance
    #                     else:
    #                         date = partial_line.credit_move_id.date if partial_line.debit_move_id == line else partial_line.debit_move_id.date
    #                         rate = line.currency_id.with_context(date=date).rate
    #                     amount_residual_currency += sign_partial_line * line.currency_id.round(partial_line.amount * rate)
    #
    #         #computing the `reconciled` field.
    #         reconciled = False
    #         digits_rounding_precision = line.move_id.company_id.currency_id.rounding
    #         if float_is_zero(amount, precision_rounding=digits_rounding_precision):
    #             if line.currency_id and line.amount_currency:
    #                 if float_is_zero(amount_residual_currency, precision_rounding=line.currency_id.rounding):
    #                     reconciled = True
    #             else:
    #                 reconciled = True
    #         line.reconciled = reconciled
    #
            # if self.round_active is True:
            #     line.amount_residual = line.move_id.company_id.currency_id.round(
            #         (amount+line.round_off_value) * sign) if line.move_id.company_id else (amount+line.round_off_value) * sign
            #     line.amount_residual_currency = line.currency_id and line.currency_id.round(
            #         amount_residual_currency * sign) or 0.0
            #
            #     # self.residual_company_signed = round(abs(line.amount_residual)+self.round_off_value) * sign
            #     # self.residual_signed = round(abs(residual)) * sign
            #     # self.residual = round(abs(residual))
            # else:
            #     line.amount_residual = line.move_id.company_id.currency_id.round(
            #         (amount + line.round_off_value) * sign) if line.move_id.company_id else (amount+line.round_off_value) * sign
            #     line.amount_residual_currency = line.currency_id and line.currency_id.round(
            #         amount_residual_currency * sign) or 0.0

                # self.residual_company_signed = abs((line.amount_residual)+self.round_off_value) * sign
                # self.residual_signed = abs(residual) * sign
                # self.residual = abs(residual)




    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        )
    def _compute_amount(self):

        super(AccountRoundOff, self)._compute_amount()
        residual = 0.0
        residual_company_signed = 0.0
        for rec in self:
            if not ('ks_global_tax_rate' in rec):
                rec.ks_calculate_discount()

            sign = rec.type in ['in_refund', 'out_refund'] and -1 or 1
            rec.amount_total_company_signed = rec.amount_total * sign
            rec.amount_total_signed = rec.amount_total * sign
            rec.residual_company_signed = rec.residual_company_signed * sign
            rec.amount_residual_signed = rec.amount_residual_signed * sign
            rec.amount_residual = rec.amount_residual




    # @api.multi
    def ks_calculate_discount(self):

        residual = 0.0
        residual_company_signed = 0.0


        for rec in self:
            if rec.type == 'entry' or rec.is_outbound():
                sign = 1
            else:
                sign = -1
            self.rounded_total = round(self.amount_untaxed + self.amount_tax)
            self.amount_total = self.amount_untaxed + self.amount_tax
            self.round_off_value = self.rounded_total - (self.amount_untaxed + self.amount_tax)

            rec.amount_total = rec.amount_tax + rec.amount_untaxed + rec.round_off_value

            for line in rec.line_ids:
                if line.account_id.internal_type in ('receivable', 'payable'):
                    residual_company_signed += line.amount_residual
                    if line.currency_id == self.currency_id:
                        residual += line.amount_residual_currency if line.currency_id else line.amount_residual
                    else:
                        from_currency = (line.currency_id and line.currency_id.with_context(
                            date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
                        residual += from_currency.compute(line.amount_residual, self.currency_id)

            if self.round_active is True:
                self.residual_company_signed = round(abs(residual_company_signed)) * sign
                self.amount_residual_signed = round(abs(residual)) * sign
                self.amount_residual = round(abs(residual))
            else:
                self.residual_company_signed = abs(residual_company_signed) * sign
                self.amount_residual_signed = abs(residual) * sign
                self.amount_residual = abs(residual)

            rec.ks_update_universal_discount()

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        ks_res = super(AccountRoundOff, self)._prepare_refund(invoice, date_invoice=None, date=None,
                                                                      description=None, journal_id=None)
        ks_res['round_off_value'] = self.round_off_value
        return ks_res

    def ks_update_universal_discount(self):
        """This Function Updates the round off through Sale Order"""
        for rec in self:
            already_exists = self.line_ids.filtered(
                lambda line: line.name and line.name.find('Round Off') == 0)
            terms_lines = self.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            other_lines = self.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
            if already_exists:
                amount = rec.round_off_value
                if rec.round_account_id \
                        and (rec.type == "out_invoice"
                             or rec.type == "out_refund") \
                        and amount > 0:
                    if rec.type == "out_invoice":
                        already_exists.update({

                            'debit': amount < 0.0 and -amount or 0.0,
                            'credit': amount > 0.0 and amount or 0.0,
                            # 'debit': amount > 0.0 and amount or 0.0,
                            # 'credit': amount < 0.0 and -amount or 0.0,
                        })
                    else:
                        already_exists.update({

                            'debit': amount > 0.0 and amount or 0.0,
                            'credit': amount < 0.0 and -amount or 0.0,
                            # 'debit': amount < 0.0 and -amount or 0.0,
                            # 'credit': amount > 0.0 and amount or 0.0,
                        })
                if rec.round_account_id \
                        and (rec.type == "in_invoice"
                             or rec.type == "in_refund") \
                        and amount > 0:
                    if rec.type == "in_invoice":
                        already_exists.update({

                            'debit': amount > 0.0 and amount or 0.0,
                            'credit': amount < 0.0 and -amount or 0.0,


                            # 'debit': amount < 0.0 and -amount or 0.0,
                            # 'credit': amount > 0.0 and amount or 0.0,
                        })
                    else:
                        already_exists.update({

                            'debit': amount < 0.0 and -amount or 0.0,
                            'credit': amount > 0.0 and amount or 0.0,
                            # 'debit': amount > 0.0 and amount or 0.0,
                            # 'credit': amount < 0.0 and -amount or 0.0,
                        })
                total_balance = sum(other_lines.mapped('balance'))
                total_amount_currency = sum(other_lines.mapped('amount_currency'))
                terms_lines.update({
                    'amount_currency': -total_amount_currency,
                    'debit': total_balance < 0.0 and -total_balance or 0.0,
                    'credit': total_balance > 0.0 and total_balance or 0.0,
                })
            if not already_exists and rec.round_off_value:
                in_draft_mode = self != self._origin
                if not in_draft_mode and rec.type:
                    rec._recompute_universal_discount_lines()
                print()

    @api.onchange('line_ids')
    def _recompute_universal_discount_lines(self):
        """This Function Create The General Entries for round off"""
        for rec in self:
            amount = self.round_off_value
            type_list = ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']
            if rec.round_off_value > 0 and rec.type in type_list:
                if rec.is_invoice(include_receipts=True):
                    in_draft_mode = self != self._origin
                    ks_name = "Round Off"

                    ks_value = ''
                    ks_name = ks_name + ks_value
                    #           ("Invoice No: " + str(self.ids)
                    #            if self._origin.id
                    #            else (self.display_name))
                    terms_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                    already_exists = self.line_ids.filtered(
                        lambda line: line.name and line.name.find('Round Off') == 0)
                    if already_exists:
                        amount = self.round_off_value
                        if self.round_account_id \
                                and (self.type == "out_invoice"
                                     or self.type == "out_refund"):
                            if self.type == "out_invoice":
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                    # 'debit': amount > 0.0 and amount or 0.0,
                                    # 'credit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                already_exists.update({

                                    # 'debit': amount > 0.0 and amount or 0.0,
                                    # 'credit': amount < 0.0 and -amount or 0.0,
                                    'name': ks_name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                        if self.round_account_id \
                                and (self.type == "in_invoice"
                                     or self.type == "in_refund"):
                            if self.type == "in_invoice":
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                    # 'debit': amount < 0.0 and -amount or 0.0,
                                    # 'credit': amount > 0.0 and amount or 0.0,
                                })
                            else:
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })
                    else:
                        new_tax_line = self.env['account.move.line']
                        create_method = in_draft_mode and \
                                        self.env['account.move.line'].new or \
                                        self.env['account.move.line'].create

                        if self.round_account_id \
                                and (self.type == "out_invoice"
                                     or self.type == "out_refund"):
                            amount = self.round_off_value
                            dict = {
                                'move_name': self.name,
                                'name': ks_name,
                                'price_unit': self.round_off_value,
                                'quantity': 1,
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                                'account_id': self.round_account_id,
                                'move_id': self._origin,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': terms_lines.partner_id.id,
                                'company_id': terms_lines.company_id.id,
                                'company_currency_id': terms_lines.company_currency_id.id,
                            }
                            if self.type == "out_invoice":
                                dict.update({
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                dict.update({
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                            if in_draft_mode:
                                self.line_ids += create_method(dict)
                                # Updation of Invoice Line Id
                                duplicate_id = self.invoice_line_ids.filtered(
                                    lambda line: line.name and line.name.find('Round Off') == 0)
                                self.invoice_line_ids = self.invoice_line_ids - duplicate_id
                            else:
                                dict.update({
                                    'price_unit': 0.0,
                                    'debit': 0.0,
                                    'credit': 0.0,
                                })
                                self.line_ids = [(0, 0, dict)]

                        if self.round_account_id \
                                and (self.type == "in_invoice"
                                     or self.type == "in_refund"):
                            amount = self.round_off_value
                            dict = {
                                'move_name': self.name,
                                'name': ks_name,
                                'price_unit': self.round_off_value,
                                'quantity': 1,
                                'debit': amount > 0.0 and amount or 0.0,
                                'credit': amount < 0.0 and -amount or 0.0,
                                'account_id': self.round_account_id,
                                'move_id': self.id,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': terms_lines.partner_id.id,
                                'company_id': terms_lines.company_id.id,
                                'company_currency_id': terms_lines.company_currency_id.id,
                            }

                            if self.type == "in_invoice":
                                dict.update({
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,

                                    # 'debit': amount < 0.0 and -amount or 0.0,
                                    # 'credit': amount > 0.0 and amount or 0.0,
                                })
                            else:
                                dict.update({
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,

                                    # 'debit': amount > 0.0 and amount or 0.0,
                                    # 'credit': amount < 0.0 and -amount or 0.0,
                                })

                            if in_draft_mode:
                                self.line_ids += create_method(dict)
                                # Updation of Invoice Line Id
                                duplicate_id = self.invoice_line_ids.filtered(
                                    lambda line: line.name and line.name.find('Round Off') == 0)
                                self.invoice_line_ids = self.invoice_line_ids - duplicate_id
                            else:
                                dict.update({
                                    'price_unit': 0.0,
                                    'debit': 0.0,
                                    'credit': 0.0,
                                })
                                self.line_ids = [(0, 0, dict)]

                            # self.line_ids += create_method(dict)
                            # # updation of invoice line id
                            # duplicate_id = self.invoice_line_ids.filtered(
                            #     lambda line: line.name and line.name.find('Round Off') == 0)
                            # self.invoice_line_ids = self.invoice_line_ids - duplicate_id

                    if in_draft_mode:
                        amount = self.round_off_value
                        # Update the payement account amount
                        terms_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                        other_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                        total_balance = sum(other_lines.mapped('balance'))
                        total_amount_currency = sum(other_lines.mapped('amount_currency'))
                        terms_lines.update({
                            'amount_currency': -total_amount_currency,
                            'debit': total_balance < 0.0 and -total_balance or 0.0,
                            'credit': total_balance > 0.0 and total_balance or 0.0,
                        })
                    else:
                        amount = self.round_off_value
                        terms_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                        other_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                        already_exists = self.line_ids.filtered(
                            lambda line: line.name and line.name.find('Round Off') == 0)
                        total_balance = sum(other_lines.mapped('balance')) + amount
                        if self.type == "out_invoice" or self.type == "out_refund":

                            total_balance = sum(other_lines.mapped('balance')) - amount
                        elif self.type == "in_invoice" or self.type == "in_refund":
                            total_balance = sum(other_lines.mapped('balance')) + amount

                        total_amount_currency = sum(other_lines.mapped('amount_currency'))
                        dict1={}
                        dict2 = {}
                        if self.type == "out_invoice" or self.type == "out_refund":
                            dict1 = {
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                            }
                            # dict1 = {
                            #     'debit': amount > 0.0 and amount or 0.0,
                            #     'credit': amount < 0.0 and amount or 0.0,
                            # }
                            dict2 = {
                                'debit': total_balance < 0.0 and -total_balance or 0.0,
                                'credit': total_balance > 0.0 and total_balance or 0.0,
                            }
                        elif self.type == "in_invoice" or self.type == "in_refund":
                            dict1 = {
                                'debit': amount > 0.0 and amount or 0.0,
                                'credit': amount < 0.0 and -amount or 0.0,
                            }

                            dict2 = {
                                'debit': total_balance < 0.0 and -total_balance or 0.0,
                                'credit': total_balance > 0.0 and total_balance or 0.0,
                            }
                        self.line_ids = [(1, already_exists.id, dict1), (1, terms_lines.id, dict2)]
                        print()


            elif rec.round_off_value < 0 and rec.type in type_list:
                if rec.is_invoice(include_receipts=True):
                    in_draft_mode = self != self._origin
                    ks_name = "Round Off"

                    ks_value = ''
                    ks_name = ks_name + ks_value
                    #           ("Invoice No: " + str(self.ids)
                    #            if self._origin.id
                    #            else (self.display_name))
                    terms_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                    already_exists = self.line_ids.filtered(
                        lambda line: line.name and line.name.find('Round Off') == 0)
                    if already_exists:
                        amount = self.round_off_value
                        if self.round_account_id \
                                and (self.type == "out_invoice"
                                     or self.type == "out_refund"):
                            if self.type == "out_invoice":
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                    # 'debit': amount > 0.0 and amount or 0.0,
                                    # 'credit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                        if self.round_account_id \
                                and (self.type == "in_invoice"
                                     or self.type == "in_refund"):
                            if self.type == "in_invoice":
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                            else:
                                already_exists.update({
                                    'name': ks_name,
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })
                    else:
                        new_tax_line = self.env['account.move.line']
                        create_method = in_draft_mode and \
                                        self.env['account.move.line'].new or \
                                        self.env['account.move.line'].create

                        if self.round_account_id \
                                and (self.type == "out_invoice"
                                     or self.type == "out_refund"):
                            amount = self.round_off_value
                            dict = {
                                'move_name': self.name,
                                'name': ks_name,
                                'price_unit': self.round_off_value,
                                'quantity': 1,
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                                'account_id': self.round_account_id,
                                'move_id': self._origin,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': terms_lines.partner_id.id,
                                'company_id': terms_lines.company_id.id,
                                'company_currency_id': terms_lines.company_currency_id.id,
                            }
                            if self.type == "out_invoice":
                                dict.update({
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                dict.update({
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                            if in_draft_mode:
                                self.line_ids += create_method(dict)
                                # Updation of Invoice Line Id
                                duplicate_id = self.invoice_line_ids.filtered(
                                    lambda line: line.name and line.name.find('Round Off') == 0)
                                self.invoice_line_ids = self.invoice_line_ids - duplicate_id
                            else:
                                dict.update({
                                    'price_unit': 0.0,
                                    'debit': 0.0,
                                    'credit': 0.0,
                                })
                                self.line_ids = [(0, 0, dict)]

                        if self.round_account_id \
                                and (self.type == "in_invoice"
                                     or self.type == "in_refund"):
                            amount = self.round_off_value
                            dict = {
                                'move_name': self.name,
                                'name': ks_name,
                                'price_unit': self.round_off_value,
                                'quantity': 1,
                                'debit': amount > 0.0 and amount or 0.0,
                                'credit': amount < 0.0 and -amount or 0.0,
                                'account_id': self.round_account_id,
                                'move_id': self.id,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': terms_lines.partner_id.id,
                                'company_id': terms_lines.company_id.id,
                                'company_currency_id': terms_lines.company_currency_id.id,
                            }

                            if self.type == "in_invoice":
                                dict.update({
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                            else:
                                dict.update({
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })

                            if in_draft_mode:
                                self.line_ids += create_method(dict)
                                # Updation of Invoice Line Id
                                duplicate_id = self.invoice_line_ids.filtered(
                                    lambda line: line.name and line.name.find('Round Off') == 0)
                                self.invoice_line_ids = self.invoice_line_ids - duplicate_id
                            else:
                                dict.update({
                                    'price_unit': 0.0,
                                    'debit': 0.0,
                                    'credit': 0.0,
                                })
                                self.line_ids = [(0, 0, dict)]

                            # self.line_ids += create_method(dict)
                            # # updation of invoice line id
                            # duplicate_id = self.invoice_line_ids.filtered(
                            #     lambda line: line.name and line.name.find('Round Off') == 0)
                            # self.invoice_line_ids = self.invoice_line_ids - duplicate_id

                    if in_draft_mode:
                        amount = self.round_off_value
                        # Update the payement account amount
                        terms_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                        other_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                        total_balance = sum(other_lines.mapped('balance'))
                        total_amount_currency = sum(other_lines.mapped('amount_currency'))
                        terms_lines.update({
                            'amount_currency': -total_amount_currency,
                            'debit': total_balance < 0.0 and -total_balance or 0.0,
                            'credit': total_balance > 0.0 and total_balance or 0.0,
                        })
                    else:
                        if self.type == "out_invoice" or self.type == "out_refund":
                            amount = self.round_off_value
                            terms_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                            other_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                            already_exists = self.line_ids.filtered(
                                lambda line: line.name and line.name.find('Round Off') == 0)
                            total_balance = sum(other_lines.mapped('balance')) - amount
                            total_amount_currency = sum(other_lines.mapped('amount_currency'))
                            dict1 = {
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                            }
                            dict2 = {
                                'debit': total_balance < 0.0 and -total_balance or 0.0,
                                'credit': total_balance > 0.0 and total_balance or 0.0,
                            }
                            self.line_ids = [(1, already_exists.id, dict1), (1, terms_lines.id, dict2)]
                            print()
                        elif self.type == "in_invoice" or self.type == "in_refund":
                            amount = self.round_off_value
                            terms_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                            other_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                            already_exists = self.line_ids.filtered(
                                lambda line: line.name and line.name.find('Round Off') == 0)
                            total_balance = sum(other_lines.mapped('balance')) + amount
                            total_amount_currency = sum(other_lines.mapped('amount_currency'))
                            dict1 = {
                                'debit': amount > 0.0 and amount or 0.0,
                                'credit': amount < 0.0 and -amount or 0.0,
                            }
                            dict2 = {
                                'debit': total_balance < 0.0 and -total_balance or 0.0,
                                'credit': total_balance > 0.0 and total_balance or 0.0,
                            }
                            self.line_ids = [(1, already_exists.id, dict1), (1, terms_lines.id, dict2)]
                            print()
                        else:
                            amount = self.round_off_value
                            terms_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                            other_lines = self.line_ids.filtered(
                                lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                            already_exists = self.line_ids.filtered(
                                lambda line: line.name and line.name.find('Round Off') == 0)
                            total_balance = sum(other_lines.mapped('balance')) - amount
                            total_amount_currency = sum(other_lines.mapped('amount_currency'))
                            dict1 = {
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                            }
                            dict2 = {
                                'debit': total_balance < 0.0 and -total_balance or 0.0,
                                'credit': total_balance > 0.0 and total_balance or 0.0,
                            }
                            self.line_ids = [(1, already_exists.id, dict1), (1, terms_lines.id, dict2)]
                            print()

            else:
                already_exists = self.line_ids.filtered(
                    lambda line: line.name and line.name.find('Round Off') == 0)
                if already_exists:
                    self.line_ids -= already_exists
                    terms_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                    other_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                    total_balance = sum(other_lines.mapped('balance'))
                    total_amount_currency = sum(other_lines.mapped('amount_currency'))
                    terms_lines.update({
                        'amount_currency': -total_amount_currency,
                        'debit': total_balance < 0.0 and -total_balance or 0.0,
                        'credit': total_balance > 0.0 and total_balance or 0.0,
                    })
