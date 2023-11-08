# -*- coding: utf-8 -*-


from odoo import fields, models


class Pharmacie(models.Model):
    _name = 'pharmacie.details'

    name = fields.Char(string='Name', required=True)
    adresse = fields.Char(string='Adresse')
    rue = fields.Char(string='Rue...')
    ville = fields.Char(string="Ville")
    etat = fields.Char(string="Etat")
    code_postal = fields.Char(string="Code Postal")
    pays = fields.Many2one('res.country', string="Pays")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Téléphone")
    email = fields.Char(sring="Email")
    site_web= fields.Char(string="Site Web")
    note_field = fields.Html(string='Comment')
    commission = fields.Float(string="Pourcentage de commission")
    logo = fields.Binary(string="Logo")
    