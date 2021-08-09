#-*- coding: utf-8-*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class MyContact(models.Model):
	# Entity name
	_name = "morales_carlos.mycontact"
	# Description of the class
	_description = "Contact in Odoo"

	# Class fields
	name = fields.Char(string='Name', required=True, copy=False, readonly=True, default=lambda self: _('New'))
	firstname = fields.Char(string='First Name', required=True)
	lastname = fields.Char(string='Last Name', required=True)
	address = fields.Text(string='Address', required=False, size=40)
	email = fields.Char(string='Email', required=True, size=40)
	phone = fields.Char(string='Phone', required=False, size=9)

	# Override create method
	@api.model
	def create(self, vals):
		if not vals.get('address'):
			vals['address'] = 'Not Specified.'

		if not vals.get('phone'):
			vals['phone'] = '999999999'
		elif 800000000 < int(vals['phone']) or int(vals['phone']) < 600000000:
			raise ValidationError(_("Phone number %s is not valid" % vals['phone']))

		# Check if email is valid
		if not bool(re.match("([a-zA-Z0-9\.]+@[a-zA-Z\.]+\.)(com|es)", vals['email'])):
			raise ValidationError(_("Email %s is not valid" % vals['email']))

		# Create ID for record
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('morales_carlos.mycontact') or _('New')

		return super(MyContact, self).create(vals)