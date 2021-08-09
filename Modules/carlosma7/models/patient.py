#-*- coding: utf-8-*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
	# Entity name
	_name = "hospital.patient"
	# Inherit from mail to get track of elements
	_inherit = ["mail.thread","mail.activity.mixin"]
	# Description of the class
	_description = "Patient of hospital"
	# Order of elements
	# _order = "doctor_id,name,age"
	_order = "age asc"

	# Class fields
	# tracking makes mail activity get recorded
	name = fields.Char(string='Name', required=True)
	reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
							default=lambda self: _('New'))
	age = fields.Integer(string='Age', required=True, tracking=True)
	gender = fields.Selection([
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other'),
		], required=True, default='other', tracking=True)
	note = fields.Text(string='Description', tracking=True)
	state = fields.Selection([
		('draft','Draft'),
		('confirm','Confirmed'),
		('done','Done'),
		('cancel','Cancelled')], default="draft", string="Status", tracking=True)
	responsible = fields.Many2one('res.partner', string="Responsible", tracking=True)
	# Computed field
	appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")
	# Image field
	image = fields.Binary(string='Patient Image')
	appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

	# Computed function
	def _compute_appointment_count(self):
		appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
		self.appointment_count = appointment_count

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
			vals['note'] = 'New Patient'
		if vals.get('reference', _('New')) == _('New'):
			vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
		return super(HospitalPatient, self).create(vals)

	# Override default get values
	@api.model
	def default_get(self, fields):
		res = super(HospitalPatient, self).default_get(fields)
		if not res.get('gender'):
			res['gender'] = 'other'
		return res

	# Constrains
	@api.constrains('name')
	def check_name(self):
		for rec in self:
			patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
			if patients:
				raise ValidationError(_("Name %s Already Exists" % rec.name))

	@api.constrains('age')
	def check_age(self):
		for rec in self:
			if rec.age == 0:
				raise ValidationError(_("Age cannot be zero!"))
			elif rec.age >= 100 or rec.age < 0:
				raise ValidationError(_("Age is not valid"))

	# Name get
	def name_get(self):
		result = []
		for rec in self:
			name = '[' + rec.reference + '] ' + rec.name
			result.append((rec.id, name))
		return result

	# Smart button box open appointments
	def action_open_appointments(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Appointments',
			'res_model': 'hospital.appointment',
			'domain': [('patient_id', '=', self.id)],
			'view_mode': 'tree,form',
			'target': 'current',
		}