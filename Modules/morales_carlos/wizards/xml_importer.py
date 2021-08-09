#-*- coding: utf-8-*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from xml.dom import minidom
from io import BytesIO
import base64
import re


# Wizard class
class ImportXMLWizard(models.TransientModel):
	_name = "import.xml.wizard"
	_description = "Import XML Wizard"

	file = fields.Binary(string="File", required=True)

	# Wizard function
	def action_import_xml(self):
		# Read every record
		xmldoc = BytesIO(base64.b64decode(self.file))
		xmldoc = minidom.parse(xmldoc)
		record_list = xmldoc.getElementsByTagName('record')
		records_vals = []

		# Get every record and check its vals
		for record in record_list:
			record_id = record.getAttribute('id')
			record_firstname = record.getElementsByTagName('field')[0].firstChild
			record_lastname = record.getElementsByTagName('field')[1].firstChild
			record_address = record.getElementsByTagName('field')[2].firstChild
			record_email = record.getElementsByTagName('field')[3].firstChild
			record_phone = record.getElementsByTagName('field')[4].firstChild

			# Check if mandatory fields exists
			if not record_firstname:
				raise ValidationError(_("Missing firstname in %s" % record_id))
			record_firstname = record_firstname.data

			if not record_lastname:
				raise ValidationError(_("Missing lastname in %s" % record_id))
			record_lastname = record_lastname.data

			if not record_email:
				raise ValidationError(_("Missing email in %s" % record_id))
			record_email = record_email.data
			# Check if email is valid
			if not bool(re.match("([a-zA-Z0-9\.]+@[a-zA-Z\.]+\.)(com|es)", record_email)):
				raise ValidationError(_("Email %s is not valid" % record_email))

			if record_address:
				record_address = record_address.data
			if record_phone:
				record_phone = record_phone.data


			vals = {
				'name': _('New'),
				'firstname': record_firstname,
				'lastname': record_lastname,
				'email': record_email,
				'address': record_address,
				'phone': record_phone
			}

			records_vals.append(vals)

		# Once all records are checked they are created
		for vals in records_vals:
			# Create a new record
			self.env['morales_carlos.mycontact'].create(vals)

		# Return updated view
		return {
			'name': _('My Contacts'),
			'type': 'ir.actions.act_window',
			'view_mode': 'tree',
			'res_model': 'morales_carlos.mycontact',
			'target': 'current',
		}

		