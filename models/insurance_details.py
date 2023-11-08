# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InsuranceDetails(models.Model):
    _name = 'insurance.details'

    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('Nouveau'))
    partner_id = fields.Many2one('res.partner', string='Employé',
                                 required=True)
    start_date = fields.Date(
        string='Date Started', default=fields.Date.context_today, required=True)
    close_date = fields.Date(string='Date Fin', readonly=True)
    invoice_ids = fields.One2many('account.move', 'insurance_id',
                                  string='Invoices', readonly=True)
    employee_id = fields.Many2one(
        'employee.details', string='Agent', required=True)
    commission_rate = fields.Float(string='Pourcentage Commission')
    policy_id = fields.Many2one(
        'policy.details', string='Police', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(related='policy_id.amount', string='Montant')
    state = fields.Selection(
        [('draft', 'Brouillon'), ('confirmed', 'Confirmé'), ('closed', 'Fermé')],
        required=True, default='draft')
    hide_inv_button = fields.Boolean(copy=False)
    note_field = fields.Html(string='Commentaire')
    policy_number = fields.Integer(string="Numéro Police", required=True,
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    famille = fields.One2many('famille.details', 'insurance_id', string='Ayant droit')
    charge = fields.One2many('charge.details', 'insurance_ids', string='Prise en charge')
    type_membre = fields.Selection(
        [('participant', 'Participant'), ('adherent', 'Adhérant'), ('honneur', 'Honneur')],
        required=True, default='participant', string="Type de membre")

    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        if self.filtered(
                lambda reward: (
                        reward.commission_rate < 0 or reward.commission_rate > 100)):
            raise ValidationError(
                _('Commission Percentage should be between 1-100'))

    @api.constrains('policy_number')
    def _check_policy_number(self):
        if not self.policy_number:
            raise ValidationError(
                _('Please add the policy number'))

    def action_confirm_insurance(self):
        if self.amount > 0:
            self.state = 'confirmed'
            self.hide_inv_button = True
        else:
            raise UserError(_("Amount should be greater than zero"))

    def action_create_invoice(self):
        created_invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': 'Facture pour Assurance',
                'quantity': 1,
                'price_unit': (self.amount*self.commission_rate)/100,
                'account_id': 41,
            })],
        })
        self.invoice_ids = created_invoice
        if self.policy_id.payment_type == 'fixed':
            self.hide_inv_button = False

    def action_close_insurance(self):
        for records in self.invoice_ids:
            if records.state == 'paid':
                raise UserError(_("All invoices must be paid"))
        self.state = 'closed'
        self.close_date = fields.Date.context_today(self)
        self.hide_inv_button = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'insurance.details') or 'New'
        return super(InsuranceDetails, self).create(vals)
