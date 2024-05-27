from odoo import api, fields, models, _

class EstatePropertyTagModel(models.Model):
	_name = "estate.property.tag"
	_description = "Estate Property Tag"
	_rec_name = "tag_name"
	_order = "tag_name"

	tag_name = fields.Char(string="Name", required=True)
	color = fields.Integer(string="Color")

	_sql_constraints = [
			('check_unique_tag_name', 'unique(tag_name)', 'Property tag name must be unique.')
		]