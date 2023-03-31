from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property tag"

    name = fields.Char("Property Tag", required=True)
