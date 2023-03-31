from odoo import models, fields, api
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
    best_price = fields.Float(compute="_best_price")
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

    type = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", copy=False)
    total_area = fields.Integer(compute="_total_area")

    @api.depends("garden_area", "living_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _best_price(self):
        for record in self:
            return max(record.offer_ids.mapped("price") or [0.00])
