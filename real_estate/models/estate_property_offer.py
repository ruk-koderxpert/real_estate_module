from odoo import api, fields, models, _, exceptions
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError


class EstatePropertyOfferModel(models.Model):
	_name = "estate.property.offer"
	_description = "Estate Property Offer"
	_order = "price desc"
	_rec_name = "property_type_id"
	# _inherit = "estate.property.offer"

	price = fields.Float(string="Price")
	status = fields.Selection([('new','New'),('accepted','Accepted'),('refused','Refused')],string="Status", required=True, copy=False, default='new')
	partner_id = fields.Many2one('res.partner', string="Partner Id", required=True)
	create_date = fields.Datetime(string="Date Time", readonly=True)
	validity = fields.Integer(string="Validity (Days)")
	date_deadline = fields.Datetime(string="Date Deadline", compute="compute_date_deadline", inverse="inverse_date_deadline", store=True)
	title = fields.Char(string="Title")
	
	expected_price = fields.Float(string="Expected Price")

	property_id = fields.Many2one('estate.property', string="Property")
	property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
	# stage = fields.Many2one('estate.property', string="Stage")


	@api.constrains('price')
	def check_expected_price(self):
		for rec in self:
			if rec.price <= 0:
				raise ValidationError(_('Please Enter Positive Price.......'))

	@api.depends('create_date', 'validity')
	def compute_date_deadline(self):
	    for rec in self:
	        if rec.create_date and rec.validity:
	            rec.date_deadline = rec.create_date + datetime.timedelta(days=rec.validity)
	        else:
	            rec.date_deadline = False  # Set to False or a default value if needed

	@api.depends('date_deadline')
	def inverse_date_deadline(self):
	    for rec in self:
	        if rec.date_deadline:
	        	if rec.create_date:
	        		rec.validity = (rec.date_deadline - rec.create_date).days
	        	else:
	        		0

	def action_accept(self):
		for rec in self:
			rec.status = 'accepted'
			rec.property_id.stage = 'offer_accepted'

	def action_refuse(self):
		for rec in self:
			rec.status = 'refused'

	# @api.model
	# def create(self, vals):
	# 	property_id = vals.get('property_id')
	# 	new_offer_amount = vals.get('price')

	# 	if property_id and new_offer_amount:
	# 		property_obj = self.env['estate.property'].browse(property_id)

	# 		existing_offers = self.search([('property_id', '=', property_id)])
	# 		for offer in existing_offers:
	# 			if offer.price >= new_offer_amount:
	# 				raise exceptions.ValidationError('You cannot create an offer with lower amount than existing offer.')

	# 		property_obj.stage = 'offer_received'
	# 	return super(EstatePropertyOfferModel, self).create(vals)