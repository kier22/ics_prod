# -*- coding: utf-8 -*-
#

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ics_meeting_count = fields.Date(related="activity_date_deadline", string="Meeting Count")
    ics_partner_id = fields.Many2one(
        'res.partner', string='Existing Customer', check_company=True, index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, "
             "TIN, Email or Internal Reference.")

