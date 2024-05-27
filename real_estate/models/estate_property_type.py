from odoo import api, fields, models, _

class EstatePropertyTypeModel(models.Model):
	_name = "estate.property.type"
	_description = "Estate Property Type"
	_rec_name = "property_type"
	_order = "property_type, sequence"

	property_type = fields.Char(name="Type", required=True, default="Abc")
	property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Id")
	sequence = fields.Integer('Sequence', default=10)
	property_count = fields.Integer(string="Property Count", compute="compute_property_count")
	
	offer_ids = fields.One2many('estate.property.offer','property_type_id', string="Offers")
	offer_count = fields.Integer(string="Offer Count", compute="compute_offer_count")

	_sql_constraints = [
				('check_unique_property_type', 'unique(property_type)', 'Property type name must be unique.')
			]

	def compute_property_count(self):
		for rec in self:
			rec.property_count = self.env['estate.property'].search_count([('property_type_id', '=', rec.id)])

	@api.depends('offer_ids')
	def compute_offer_count(self):
		for record in self:
			# rec.offer_count = self.env['estate.property.offer'].search_count([('property_id.property_type_id', '=', rec.id)])
			record.offer_count = len(record.offer_ids)

	def action_view_properties(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Properties',
			'view_mode': 'tree,form',
			'res_model': 'estate.property',
			'domain': [('property_type_id', '=', self.id)],
			'context': {'default_property_type_id': self.id},
		}

	def action_view_offers(self):
		properties = self.env['estate.property'].search([('property_type_id', '=', self.id)])
		return {
			'type': 'ir.actions.act_window',
			'name': 'Offers',
			'view_mode': 'tree,form',
			'res_model': 'estate.property.offer',
			'domain': [('partner_id', 'in', properties.ids)],
			'context': {'default_partner_id': self.env.context.get('default_partner_id')},
		}