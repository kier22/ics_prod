from odoo import api, fields, models


class DayTag(models.Model):
    _name = 'day.tag'
    _description = 'Days of the week'

    name = fields.Char(string='Name', required=True)
    day_tag_id = fields.Many2one('res.partner')
