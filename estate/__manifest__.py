{
    "name": "estate",
    "summary": "Real Estate management",
    "author": "Johan",
    "website": "https://odoo.fr",
    "category": "Website",
    "version": "12.0.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "data/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
