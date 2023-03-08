# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ics_auto_price_ok = fields.Boolean('Auto Price Set', default=False)
