from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=lambda self: fields.Date.to_string(
            fields.Datetime.today() + relativedelta(months=3)
        ),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("North", "North"),
            ("South", "South"),
            ("West", "West"),
            ("East", "East"),
        ],
        help="Select an orientation",
    )
    active = fields.Boolean(default=True)

    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Canceled", "Canceled"),
        ],
        help="Property status",
        required=True,
        copy=False,
        default="new",
    )
