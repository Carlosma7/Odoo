#-*- coding: utf-8-*-

from odoo import api, fields, models, _

# Wizard class
class CreateAppointmentWizard(models.TransientModel):
	_name = "create.appointment.wizard"
	_description = "Create Appointment Wizard"

	date_appointment = fields.Date(string='Date', required=False)
	patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

	# Wizard function
	def action_create_appointment(self):
		print("Wizard button is clicked")
		vals = {
			'patient_id': self.patient_id.id,
			'date_appointment': self.date_appointment
		}
		# Create a new record
		appointment_rec = self.env['hospital.appointment'].create(vals)

		return {
			'name': _('Appointment'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'hospital.appointment',
			'res_id': appointment_rec.id,
		}

	# View appointment
	def action_view_appointment(self):
		# Method 1
		# action = self.env.ref('carlosma7.action_hospital_appointment').read()[0]
		# action['domain'] = [('patient_id', '=', self.patient_id.id)]
		# return action

		# Method 2
		# action = self.env.['ir.actions.actions']._for_xml_id('carlosma7.action_hospital_appointment')
		# action['domain'] = [('patient_id', '=', self.patient_id.id)]
		# return action

		# Method 3
		return {
			'type': 'ir.actions.act_window',
			'name': 'Appointments',
			'res_model': 'hospital.appointment',
			'view_type': 'form',
			'domain': [('patient_id', '=', self.patient_id.id)],
			'view_mode': 'tree,form',
			'target': 'current',
		}