#-*- coding: utf-8 -*-


from odoo import fields, models



class ProductCommande(models.Model):
    _name = 'product.order'

    num_order = fields.Char(string = 'Numéro Commande')
    quantity= fields.Integer(string = 'Quantité')
    designation = fields.Char( string = 'Désignation')
    prix_unitaire = fields.Float(string = 'Prix Unitaire')
    prix_total = fields.Float(string = 'Prix Total')
    montant_total = fields.Float( string= 'Montant Total')
    order_id = fields.Many2one('order.details', string='Bon de commande')
    