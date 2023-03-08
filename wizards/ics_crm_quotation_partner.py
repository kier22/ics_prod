from odoo import api, fields, models, exceptions, UserError


class Opportunity2Quotation(models.TransientModel):
    _inherit = 'crm.quotation.partner'
