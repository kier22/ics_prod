from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    ics_campaign_id = fields.Many2one('utm.campaign', string='Campaign')
    ics_source_id = fields.Many2one('utm.source', string='Source')
    ics_cleaning_frequency = fields.Selection(string='Cleaning Frequency',
                                              selection=[('weekly', 'weekly'),
                                                         ('fortnightly', 'fortnightly'),
                                                         ('monthly', 'monthly'),
                                                         ('one off', 'one off')])

    """ Added to support the email template for ICS 05.02.23 """

    ics_cost_per = fields.Selection(string='Cost Per',
                                    selection=[('day', 'day'),
                                               ('week', 'week'),
                                               ('month', 'month'),
                                               ('visit', 'visit')])
    ics_day_tags_ids = fields.Many2many(comodel_name="day.tag", string="Cleaning Days")
    ics_total_hrs_per_freq = fields.Float(string='Total Hours Per Frequency')
    ics_hrs_per_day = fields.Float(string='Hours Per Day')
    ics_wage_per_hr = fields.Float(string='Wage Per Hour')
    ics_hr_notes = fields.Text(string='Hour Notes')
