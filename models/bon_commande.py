#-*- coding: utf-8 -*-


from odoo import fields, models


class BonCommande(models.Model):
    _name = 'order.details'
    insurance_id = fields.Many2one('insurance.details',  
        string='Assurance')
    num_order = fields.Char(string = 'Numéro Commande')
    product = fields.One2many('product.order', 'order_id', string = 'Commande')
    beneficiaire = fields.Char( string='Bénéficiaire')
    Ordonnance = fields.Char(string='Ordonnance')
    police = fields.Integer(related='insurance_id.policy_number', string='Numéro de Police')
    participant = fields.Char()
    commission = fields.Float(related='insurance_id.commission_rate', string='Pourcentage de commission')
    date_commande = fields.Date(string ='Date de commande')
