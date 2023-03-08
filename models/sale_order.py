# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Populates the line start date based on today's date by default, user can extend period by overriding date
    # Populates the line end date by 1 year by default, user can extend period by overriding date

    ics_line_date_start = fields.Date(string='Start Date', default=(datetime.datetime.now()))
    ics_line_date_end = fields.Date(string='End Date')
    ics_auto_price_ok = fields.Boolean(related='product_id.ics_auto_price_ok', store=True)

    # removed 19/08/22 default=(datetime.datetime.today().date() + datetime.timedelta(12 * 365 / 12)).isoformat())

    ics_subscription = fields.Selection(related='order_id.ics_subscription', store=True)


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    sale_order_id = fields.Many2one('sale.order', 'id')


class ContractLine(models.Model):
    _inherit = 'contract.line'

    order_line_id = fields.Many2one('sale.order.line', 'id')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ics_subscription = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Subscription', required=True)
    ics_contract_id = fields.Many2one('contract.contract', 'id')
    invoice_status = fields.Selection(selection_add=[('no_invoice', 'Invoice Not Applicable')])

    # Create contract on confirmation of SO

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        if self.ics_subscription == 'yes':
            contract_id = self.env['contract.contract'].create({
                'sale_order_id': self.id,
                'name': self.name,
                'partner_id': self.partner_id.id,
                'code': self.name,
                'payment_term_id': self.payment_term_id.id,
                'line_recurrence': True
            })

            # Captures the contract ID, so it can be used later when adding the lines to the contract
            last_id = contract_id.id
            self.write({'ics_contract_id': last_id})

            for record in self.order_line:
                contractline_ids = self.env['contract.line'].create({
                    "product_id": record.product_id.id,
                    "name": record.product_id.name,
                    "quantity": record.product_uom_qty,
                    "uom_id": record.product_uom.id,
                    "price_unit": record.price_unit,
                    "discount": record.discount,
                    "contract_id": last_id,
                    "order_line_id": record.id,
                    "date_start": record.ics_line_date_start,
                    "date_end": record.ics_line_date_end,
                    "recurring_rule_type": 'monthlylastday',
                    "recurring_invoicing_type": 'post-paid',
                    "automatic_price": record.product_id.ics_auto_price_ok,
                    "manual_renew_needed": True
                })

    # Override the duplicate method to remove the contract id when duplicating a quote/sales order

    def copy_data(self, default=None):
        if default is None:
            default = {}
        if 'order_line' not in default:
            default.update({'ics_contract_id': '',
                            'ics_subscription': 'no'})
        return super(SaleOrder, self).copy_data(default)
