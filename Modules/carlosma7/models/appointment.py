#-*- coding: utf-8-*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
	# Entity name
	_name = "hospital.appointment"
	# Inherit from mail to get track of elements
	_inherit = ["mail.thread","mail.activity.mixin"]
	# Description of the class
	_description = "Hospital Appointment"

	# Class fields
	# tracking makes mail activity get recorded
	name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
							default=lambda self: _('New'))
	patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
	# Related field to another class
	age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
	doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
	# Field for onchange
	gender = fields.Selection([
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other'),
		], string='Gender')
	state = fields.Selection([
		('draft','Draft'),
		('confirm','Confirmed'),
		('done','Done'),
		('cancel','Cancelled')], default="draft", string="Status", tracking=True)
	note = fields.Text(string='Description', tracking=True)
	date_appointment = fields.Date(string="Date")
	date_checkup = fields.Datetime(string="Check Up Time")
	prescription = fields.Text(string="Prescription")
	# One2many
	prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id', string="Prescription Lines")
	
	# Button actions
	def action_confirm(self):
		print("Clicked on button confirm")
		self.state = "confirm"

	def action_done(self):
		print("Clicked on button done")
		self.state = "done"

	def action_draft(self):
		print("Clicked on button draft")
		self.state = "draft"

	def action_cancel(self):
		print("Clicked on button cancel")
		self.state = "cancel"

	# Override create method
	@api.model
	def create(self, vals):
		if not vals.get('note'):
			vals['note'] = 'New Appointment'
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
		return super(HospitalAppointment, self).create(vals)

	# Onchange patient id method
	@api.onchange('patient_id')
	def onchange_patient_id(self):
		print('onchange_triggered')
		if self.patient_id:
			if self.patient_id.gender:
				self.gender = self.patient_id.gender
		else:
			self.gender = ''

	# Unlink override
	def unlink(self):
		print("Deleting the Record")
		if self.state == 'done':
			raise ValidationError(_("You Cannot Delete %s as it is in Done State", self.name))
		return super(HospitalAppointment, self).unlink()

	# Url Link
	def action_url(self):
		module_name = 'om_hospital'
		return {
			'type': 'ir.actions.act_url',
			'target': 'new',
			'url': 'https://apps.odoo.com/apps/modules/14.0/%s/' % module_name,
		}

class AppointmentPrescriptionLines(models.Model):
	_name = "appointment.prescription.lines"
	_description = "Appointment Prescription Lines"

	name = fields.Char(string="Medicine", required=True)
	qty = fields.Integer(string="Quantity", required=True)
	appointment_id = fields.Many2one('hospital.appointment', string="Appointment")