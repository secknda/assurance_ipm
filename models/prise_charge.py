# -*- coding: utf-8 -*-

from odoo import fields, models, api, _ 


class PriseCharge(models.Model):
    _name = 'charge.details'

    reference = fields.Selection(
        [('hopital', 'Hopital'),('pharmacie', 'Pharmacie'), ('clinique', 'Clinique'),('opticien', 'Opticien'), ('praticien', 'Praticien')],
        required=True, default='hopital')
    hopital = fields.Many2one(
        'hopital.details', string="Nom de l'Hopital")
    praticien = fields.Many2one(
        'praticien.details', string='Nom du Praticien')
    opticien = fields.Many2one(
        'opticien.details', string="Nom de l'Opticien")
    clinique = fields.Many2one(
        'clinique.details', string='Nom de la Clinique')
    phamacie = fields.Many2one(
        'phamacie.details', string='Nom de la Phamacie')
    insurance_ids = fields.Many2one(
        'insurance.details', string='Assurance')
    commission = fields.Float(string = 'Pourcentage Commission', compute='_compute_commission')
    nom_ref = fields.Char(string = 'Nom de la réference', compute='_valide_name_ref')

    @api.depends('reference', 'hopital.commission','clinique.commission','opticien.commission','praticien.commission')
    def _compute_commission(self):
        for record in self:
            if record.reference == 'hopital' and record.hopital:
                record.commission = record.hopital.commission
            elif record.reference == 'clinique' and record.clinique:
                record.commission = record.clinique.commission
            elif record.reference == 'opticien' and record.opticien:
                record.commission = record.opticien.commission
            elif record.reference == 'praticien' and record.praticien:
                record.commission = record.praticien.commission
            elif record.reference == 'pharmacie' and record.pharmacie:
                record.commission = record.pharmacie.commission
            else:
                record.commission = 1.0
    
    
    @api.depends('reference', 'hopital.name','clinique.name','opticien.name','praticien.name')
    def _valide_name_ref(self):
        for record in self:
            if record.reference == 'hopital' and record.hopital:
                record.nom_ref = record.hopital.name
            elif record.reference == 'clinique' and record.clinique:
                record.nom_ref = record.clinique.name
            elif record.reference == 'opticien' and record.opticien:
                record.nom_ref = record.opticien.name
            elif record.reference == 'praticien' and record.praticien:
                record.nom_ref = record.praticien.name
            elif record.reference == 'pharmacie' and record.pharmacie:
                record.nom_ref = record.pharmacie.name
            else:
                record.nom_ref = ''
    