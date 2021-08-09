# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Class for project management and their relationships
class Projects(models.Model):
	# Name of table
	_name = "projects.project"

	# Simple fields of the object
	name = fields.Char(string="Project title", required=True)
	identifier = fields.Char(string="ID", required=True)
	locality = fields.Char(string="Locality")
	province = fields.Char(string="Province")
	start_date = fields.Date(string="Start date")

	# Relational fields with other classes
	department_ids = fields.Many2one('projects.department', string="Department")	# department_id
	employee_id = fields.Many2many('projects.employee', string="Employees")	# employee_ids

	# Constraint of the employees working in the project
	@api.constrains('employee_id')
	@api.multi
	def _check_department(self):
		for record in self:
			# If we have a department
			if record.department_ids:
				# Iterate over all employees selected for the project
				for employee_x in record.employee_id:
					# If any of the employees doesn't belong to the same department of the project, then raise a ValidationError
					if employee_x.department_id.name is not record.department_ids.name:
						raise ValidationError("Employee %s is not valid because he doesn't belong to the project's department." % employee_x.name)

# Extension Class for the project class
class PriorityProjects(models.Model):
	# We inherit from the project class and use the same table
	_inherit = 'projects.project'

	# Add a new field to save the deadline of a project
	limit_date = fields.Date(string="Limit date", required=True)