# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime


class ContractLine(models.Model):
    _inherit = 'contract.line'

    pricelist_id = fields.Many2one('product.pricelist', 'id')
    fiscal_position_id = fields.Many2one('account.fiscal.position', 'id')
    automatic_price = fields.Boolean('Auto-Price?')
    ics_analytic_tag_ids = fields.Many2one('account.analytic.tag', 'id')
    ics_analytic_account_id = fields.Many2one('account.analytic.account', 'id')

    ics_obsolete_line = fields.Boolean(string='Obsolete Line',
                                       store=True,
                                       readonly=False
                                       )


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    to_renew = fields.Boolean('To Renew')

    contract_line_ids = fields.One2many(
        string="Contract lines",
        comodel_name="contract.line",
        inverse_name="contract_id",
        copy=True, domain=[('ics_obsolete_line', '!=', True)]
    )

    contract_line_fixed_ids = fields.One2many(
        string="Contract lines (fixed)",
        comodel_name="contract.line",
        inverse_name="contract_id"
    )

    class ContractAbstractContractLine(models.AbstractModel):
        _inherit = 'contract.abstract.contract.line'

        ics_automatic_price = fields.Boolean(related='product_id.ics_auto_price_ok')
        ics_price_unit = fields.Float(
            string="Unit Price",
            compute="_compute_price_unit",
            inverse="_inverse_price_unit",
        )

        """ 20/01/23 - Override the base function _compute_price_unit from contract.abstract.contract.line
            to set the price_unit from the product template based on the new field ics_automatic_price """

        def _compute_price_unit(self):
            """Get the specific price if no auto-price, and the price obtained
            from the pricelist otherwise.
            """
            for line in self:
                if line.ics_automatic_price:
                    pricelist = (
                            line.contract_id.pricelist_id
                            or line.contract_id.partner_id.with_company(
                        line.contract_id.company_id
                    ).property_product_pricelist
                    )
                    product = line.product_id.with_context(
                        quantity=line.env.context.get(
                            "contract_line_qty",
                            line.quantity,
                        ),
                        pricelist=pricelist.id,
                        partner=line.contract_id.partner_id.id,
                        date=line.env.context.get(
                            "old_date", fields.Date.context_today(line)
                        ),
                    )
                    line.price_unit = product.price
                else:
                    line.price_unit = line.specific_price

        """ 20/01/23 - Override the base function _inverse_price_unit from contract.abstract.contract.line
            to set the price_unit from the product template based on the new field ics_automatic_price """

        @api.onchange("price_unit")
        def _inverse_price_unit(self):
            """Store the specific price in the no auto-price records."""
            for line in self.filtered(lambda x: not x.ics_automatic_price):
                line.specific_price = line.price_unit

        ics_obsolete_line = fields.Boolean(string='Obsolete Line',
                                           store=True,
                                           readonly=False
                                           )

    class ContractRecurrencyBasicMixin(models.AbstractModel):
        _inherit = "contract.recurrency.basic.mixin"

        """ 20/01/23 - Override the base field recurring_rule_type from contract.recurrency.basic.mixin
            to set the default value to Month(s) last day """

        recurring_rule_type = fields.Selection(
            [
                ("daily", "Day(s)"),
                ("weekly", "Week(s)"),
                ("monthly", "Month(s)"),
                ("monthlylastday", "Month(s) last day"),
                ("quarterly", "Quarter(s)"),
                ("semesterly", "Semester(s)"),
                ("yearly", "Year(s)"),
            ],
            default="monthlylastday",
            string="Recurrence",
            help="Specify Interval for automatic invoice generation.",
        )

        """ 20/01/23 - Override the base field recurring_invoicing_type from contract.recurrency.basic.mixin
            to set the default value to Post-paid """

        recurring_invoicing_type = fields.Selection(
            [("pre-paid", "Pre-paid"), ("post-paid", "Post-paid")],
            default="post-paid",
            string="Invoicing type",
            help=(
                "Specify if the invoice must be generated at the beginning "
                "(pre-paid) or end (post-paid) of the period."
            ),
        )
