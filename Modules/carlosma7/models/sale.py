# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
	_inherit = "sale.order"

	# Override class with new field
	sale_description = fields.Char(string='Sale Description')