from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property type"

    name = fields.Char("Property Type", required=True)
