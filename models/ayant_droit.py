# -*- coding: utf-8 -*-


from odoo import fields, models


class Famille(models.Model):
    _name = 'famille.details'

    name = fields.Char(string='Prénom et Nom', required=True)
    prenom = fields.Char(string='Prénom')
    adresse = fields.Char(string='Adresse')
    image = fields.Binary(string='Photo')
    date_naissance = fields.Date(string="Date de Naissance")
    lieu_naissance = fields.Char(string="Lieu de Naissance")
    phone = fields.Char(string="Numéro de Téléphone")
    email = fields.Char(string="Email")
    ville = fields.Char(string="Ville")
    num_security = fields.Char(string="Numéro Sécurité sociale")
    lien = fields.Selection(
        [('epoux', 'Epoux/Epouse'), ('fils', 'Fils/Fille'), ('pere', 'Père/Mère')],
        required=True,)
    bulletin = fields.Binary(string ="Bulletin de Naissance")
    note_field = fields.Html(string='Note Interne')
    sexe = fields.Selection(
        [('masculin', 'Masculin'), ('feminin', 'Féminin')],
        required=True, default='masculin')
    insurance_id=fields.Many2one('insurance.details',string="Liste assurances")
    

    