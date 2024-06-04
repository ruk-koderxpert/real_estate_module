from odoo import models, fields, api

class EstateProperty(models.Model):
	_inherit = "estate.property"

	def action_sold(self):
		res = super(EstateProperty, self).action_sold()

		selling_price = self.selling_price
		commission = selling_price * 0.06
		admin_fee = 100.00

		self.env['account.move'].sudo().create({
				'partner_id': self.buyer.id,
				'move_type': 'out_invoice',
				'invoice_line_ids':[
					(0, 0, {
						'name': 'Commission (6% of Selling Price)',
						'quantity': 1,
						'price_unit': commission
					}),
					(0, 0,{
						'name': 'Administrative Fees',
						'quantity': 1,
						'price_unit': admin_fee,
					}),
				]

			})
		return True
