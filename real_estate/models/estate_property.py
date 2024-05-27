from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class EstatePropertyModel(models.Model):
	_name = "estate.property"
	_description = "Estate Property"
	_rec_name = "title"
	_order = "id desc"

	title = fields.Char(string="Title", default="unknown")
	note = fields.Text(string="Description")
	
	property_type_id = fields.Many2one('estate.property.type', string="Property Type", required=True)
	postcode = fields.Char(string="Postcode")
	expected_price = fields.Float(string="Expected Price")
	best_price = fields.Float(string="Best Offer", compute="compute_best_price")
	bedrooms = fields.Integer(default="2")
	facades = fields.Integer(string="Facades")
	garden = fields.Boolean(string="Garden")
	garden_orientation = fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')], string="Garden Orientation")

	available_from = fields.Datetime("Available From", default=fields.Datetime.now, readonly=True)
	selling_price = fields.Float(string="Selling Price", compute="compute_selling_price")
	living_area = fields.Integer(string="Living Area(sqm)")
	garage = fields.Boolean(string="Garage")
	garden_area = fields.Integer(string="Garden Area(sqm)")
	active = fields.Boolean(string="Active", default=True)

	salesman = fields.Char(string="Salesperson", default="Amit")
	buyer = fields.Many2one('res.partner', string="Buyer")

	tag_ids = fields.Many2many('estate.property.tag', string="Tags")
	offer_ids = fields.One2many('estate.property.offer','property_id', string="Offer Id")
	total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_result")

	price = fields.Many2one('estate.property.offer', string="Prices", required=True)
	# states = fields.Selection([('new','New'),('sold','Sold'),('cancel','Cancel')], default="new", string="State", tracking=True)

	count = fields.Many2one('estate.property.type', string="Count")
	stage = fields.Selection([('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancel','Cancel')], default="new", string="Stage", readonly=True, tracking=True)

	@api.constrains('expected_price')
	def check_expected_price(self):
		for rec in self:
			if rec.expected_price <= 0:
				raise ValidationError(_('Please Enter Positive Expected Price.......'))

	@api.constrains('selling_price')
	def check_expected_price(self):
		for rec in self:
			if rec.selling_price <= 0:
				raise ValidationError(_('Please Enter Positive Selling Price.......'))

	@api.constrains('best_price')
	def check_best_price(self):
		for rec in self:
			if rec.best_price <= 0:
				raise ValidationError(_('Please Enter Positive Best Price.......'))


	def copy(self, default=None):
		if default is None:
			default={}
		if not default.get('available_from'):
			default['available_from'] = _("%s (Copy)",self.available_from)
		return super(EstatePropertyModel,self).copy(default)

	def copy(self, default=None):
		if default is None:
			default={}
		if not default.get('buyer'):
			default['buyer'] = _("%s (Copy)",self.buyer)
		return super(EstatePropertyModel,self).copy(default)

	@api.depends('living_area', 'garden_area')
	def _compute_result(self):
		for rec in self:
			rec.total_area = rec.living_area + rec.garden_area

	@api.depends('offer_ids.price')
	def compute_best_price(self):
	    for record in self:
	        if record.offer_ids:
	            record.best_price = max(offer.price for offer in record.offer_ids)
	        else:
	            record.best_price = 0.0  # or any default value you prefer


	@api.onchange('garden')
	def onchange_garder_area(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = 'north'
		else:
			self.garden_area = 0
			self.garden_orientation = False


	def action_sold(self):
		for rec in self:
			if rec.stage == 'cancel':
				raise ValidationError(_("Can't change States for Sold....."))
			rec.stage = 'sold'
			rec.offer_ids.status = 'accepted'

	def action_cancel(self):
		for rec in self:
			if rec.stage == 'sold':
				raise ValidationError(_("Can't change States for cancel....."))
			rec.stage = 'cancel'
			rec.offer_ids.status = 'cancel'

	@api.depends('offer_ids')
	def compute_selling_price(self):
		for offer in self.offer_ids:
			if offer.status == 'accepted':
				self.buyer = offer.partner_id
				# self.states = self.states['offer_accepted']
				
				self.selling_price = offer.price
				break
		else:
			self.selling_price = self.expected_price

	@api.constrains('selling_price', 'expected_price')
	def _check_selling_price(self):
		for product in self:
			if product.selling_price < 0.9 * product.expected_price:
				raise ValidationError("Selling price cannot be lower than 90% of the expected price.")


