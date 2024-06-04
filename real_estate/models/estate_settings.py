from odoo import models, fields

class EstateSettings(models.Model):
    _name = 'estate.settings'
    _description = 'Estate Settings'

    name = fields.Char(string='Name', required=True)
    # Add other fields as necessary