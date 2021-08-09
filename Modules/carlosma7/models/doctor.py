# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
	_name = "hospital.doctor"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "Hospital Doctor"
	# Rec name for variable instead of "name"
	_rec_name = 'doctor_name'

	doctor_name = fields.Char(string='Name', required=True, tracking=True)
	# Copy field false
	age = fields.Integer(string='Age', tracking=True, copy=False)
	gender = fields.Selection([
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other'),
		], required=True, default='other', tracking=True)
	note = fields.Text(string='Description')
	image = fields.Binary(string='Doctor Image')
	# Computed field
	appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")

	# Computed function
	def _compute_appointment_count(self):
		appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', self.id)])
		self.appointment_count = appointment_count

	# Override copy method
	def copy(self, default=None):
		print("Successfully Copied")

		if default is None:
			default = {}
		if not default.get('doctor_name'):
			default['doctor_name'] = _("%s (Copy)", self.doctor_name)
		default['note'] = "Copied Record"
		return super(HospitalDoctor, self).copy(default)

	# Smart button box open appointments
	def action_open_appointments(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Appointments',
			'res_model': 'hospital.appointment',
			'domain': [('doctor_id', '=', self.id)],
			'view_mode': 'tree,form',
			'target': 'current',
		}