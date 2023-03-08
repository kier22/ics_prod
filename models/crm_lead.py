# -*- coding: utf-8 -*-
#

from odoo import api, fields, models, tools


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ics_meeting_count = fields.Date(related="activity_date_deadline", string="Meeting Count")

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


class Lead(models.Model):
    _inherit = 'crm.lead'

    def _find_matching_partner(self, email_only=False):
        """ Try to find a matching partner with available information on the
        lead, using notably customer's name, email, ...

        :param email_only: Only find a matching based on the email. To use
            for automatic process where ilike based on name can be too dangerous
        :return: partner browse record
        """
        self.ensure_one()
        partner = self.partner_id

        if not partner and self.email_from:
            partner = self.env['res.partner'].search([('email', '=', self.email_from)], limit=1)

        if not partner and not email_only:
            # search through the existing partners based on the lead's partner or contact name
            # to be aligned with _create_customer, search on lead's name as last possibility
            for customer_potential_name in [self[field_name] for field_name in ['partner_name', 'contact_name', 'name']
                                            if self[field_name]]:
                partner = self.env['res.partner'].search([('name', 'ilike', '%' + customer_potential_name + '%')],
                                                         limit=1)
                if partner:
                    break

        return partner

    def _create_customer(self):
        """ Create a partner from lead data and link it to the lead.

        :return: newly-created partner browse record
        """
        Partner = self.env['res.partner']
        contact_name = self.contact_name
        if not contact_name:
            contact_name = Partner._parse_partner_name(self.email_from)[0] if self.email_from else False

        if self.partner_name:
            partner_company = Partner.create(self._prepare_customer_values(self.partner_name, is_company=True))
        elif self.partner_id:
            partner_company = self.partner_id
        else:
            partner_company = None

        if contact_name:
            return Partner.create(self._prepare_customer_values(contact_name, is_company=False,
                                                                parent_id=partner_company.id if partner_company else False))

        if partner_company:
            return partner_company
        return Partner.create(self._prepare_customer_values(self.name, is_company=False))

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """ Extract data from lead to create a partner.

        :param name : furtur name of the partner
        :param is_company : True if the partner is a company
        :param parent_id : id of the parent partner (False if no parent)
        :return: dictionary of values to give at res_partner.create()

        :15/02/23 added visit info fields to copy to company
        """
        email_parts = tools.email_split(self.email_from)
        res = {
            'name': partner_name,
            'user_id': self.env.context.get('default_user_id') or self.user_id.id,
            'comment': self.description,
            'team_id': self.team_id.id,
            'parent_id': parent_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': email_parts[0] if email_parts else False,
            'title': self.title.id,
            'function': self.function,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id.id,
            'state_id': self.state_id.id,
            'website': self.website,
            'is_company': is_company,
            'type': 'contact',
            'ics_cleaning_frequency': self.ics_cleaning_frequency,
            'ics_cost_per': self.ics_cost_per,
            'ics_day_tags_ids': self.ics_day_tags_ids,
            'ics_total_hrs_per_freq': self.ics_total_hrs_per_freq,
            'ics_hrs_per_day': self.ics_hrs_per_day,
            'ics_wage_per_hr': self.ics_wage_per_hr,
            'ics_hr_notes': self.ics_hr_notes

        }
        if self.lang_id:
            res['lang'] = self.lang_id.code
        return res
