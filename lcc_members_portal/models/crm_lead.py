from odoo import fields, models, api
from odoo.tools.translate import _


class Lead(models.Model):
    _inherit = "crm.lead"

    _MAIN_PROFILE_FIELDS = [
        "website_description",
        "street",
        "street2",
        "city",
        "zip",
        "country_id",
        "team_id",
        "phone",
        "company_email",
        "website",
        "industry_id",
        "accept_digital_currency",
        "accept_coupons",
        "want_newsletter_subscription",
        "accept_policy",
    ]

    _PUBLIC_PROFILE_FIELDS = [
        "website_description",
        "street",
        "street2",
        "city",
        "zip",
        "country_id",
        "team_id",
        "phone",
        "company_email",
        "website",
        "industry_id",
        "detailed_activity",
        "reasons_choosing_mlc",
        "opening_time",
        "discount",
        "itinerant",
        "accept_digital_currency",
        "accept_coupons",
    ]

    _POSITION_PROFILE_FIELDS = [
        "function",
        "phone_pro",
    ]

    lead_type = fields.Selection(
        [
            ("misc", "Miscellenaous"),
            ("membership_web_application", "Membership Web Application"),
        ],
        string="Lead Type",
        required=True,
        readonly=True,
        copy=False,
        default="misc",
    )

    company_name = fields.Char(string=_("Company Name"))
    commercial_company_name = fields.Char(string=_("Commercial Company Name"))
    website_description = fields.Html(string=_("Website Description"), strip_style=True)
    company_email = fields.Char(string=_("Email"))
    industry_id = fields.Many2one("res.partner.industry", string=_("Main activity"))
    detailed_activity = fields.Char(string=_("Detailed activity"))
    reasons_choosing_mlc = fields.Text(string=_("Why did I choose local currency"))
    opening_time = fields.Text(string=_("Opening Time"))
    discount = fields.Html(string=_("Discount"))
    accept_digital_currency = fields.Boolean(string=_("Accept digital currency"))
    accept_coupons = fields.Boolean(string=_("Accept coupons"))
    itinerant = fields.Boolean(string=_("Itinerant"))
    function = fields.Char(string=_("Job Position"))
    phone_pro = fields.Char(string=_("Phone Pro"))
    want_newsletter_subscription = fields.Boolean(
        string=_("Want Newsletters Subscription")
    )
    accept_policy = fields.Boolean(string=_("Accept LCC Policy"))
    total_membership = fields.Float(string=_("Membership amount"))
    message_from_candidate = fields.Text(string=_("Message from the candidate"))

    def _get_field_value(self, fname):
        field = self._fields[fname]
        if field.type == "many2one":
            return self[fname].id
        elif field.type == "one2many":
            return None
        elif field.type == "many2many":
            return [(6, 0, self[fname].ids)]
        else:
            return self[fname]

    @api.multi
    def action_validate_organization_application(self):

        # Organization's main partner creation
        values = {}
        for field_name in self._MAIN_PROFILE_FIELDS:
            values[field_name] = self._get_field_value(field_name)
        values["name"] = self.commercial_company_name
        values["is_company"] = True
        values["partner_profile"] = (
            self.env["partner.profile"]
            .search([("ref", "=", "partner_profile_main")], limit=1)
            .id
        )
        values["type"] = "contact"
        values.update({"email": values.pop("company_email", "")})
        main_partner = self.env["res.partner"].create(values)

        # Organization's public partner creation
        values = {}
        for field_name in self._PUBLIC_PROFILE_FIELDS:
            values[field_name] = self._get_field_value(field_name)
        values["name"] = self.commercial_company_name
        values["is_company"] = True
        values["contact_id"] = main_partner.id
        values["partner_profile"] = (
            self.env["partner.profile"]
            .search([("ref", "=", "partner_profile_public")], limit=1)
            .id
        )
        values["type"] = "contact"
        values.update({"email": values.pop("company_email", "")})
        self.env["res.partner"].create(values)

        # Organization's contact's position partner creation
        values = {}
        for field_name in self._POSITION_PROFILE_FIELDS:
            values[field_name] = self._get_field_value(field_name)
        values["name"] = self.contact_name
        values["is_company"] = False
        values["contact_id"] = self.partner_id.id
        values["parent_id"] = main_partner.id
        values["partner_profile"] = (
            self.env["partner.profile"]
            .search([("ref", "=", "partner_profile_position")], limit=1)
            .id
        )
        values["type"] = "contact"
        values["edit_structure_main_profile"] = True
        values["edit_structure_public_profile"] = True
        values.update({"phone": values.pop("phone_pro", "")})
        self.env["res.partner"].create(values)

        # Redirect to the main profile
        view = self.env.ref("base.view_partner_form")
        return {
            "name": "Partners created",
            "view_type": "form",
            "view_mode": "form",
            "view_id": view.id,
            "res_model": "res.partner",
            "type": "ir.actions.act_window",
            "res_id": main_partner.id,
            "context": self.env.context,
        }