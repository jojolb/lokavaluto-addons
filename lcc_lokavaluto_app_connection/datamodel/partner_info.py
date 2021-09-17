from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class PartnerInfoGetParam(Datamodel):
    _name = "partner.info.get.param"

    website_url = fields.String(required=False, allow_none=True)
    backend_keys = fields.List(fields.String())


class PartnerSearchInfo(Datamodel):
    _name = "partner.search.info"

    value = fields.String(required=False, allow_none=True)
    backend_keys = fields.List(fields.String())
    is_favorite = fields.Boolean(required=False, allow_none=True)
    is_company = fields.Boolean(required=False, allow_none=True)
    offset = fields.Integer(required=False, allow_none=True)
    limit = fields.Integer(required=False, allow_none=True)
    website_url = fields.String(required=False, allow_none=True)
    order = fields.String(required=False, allow_nano=True)
