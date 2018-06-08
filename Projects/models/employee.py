# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Class for employees management and their relationships
class Employees(models.Model):
	# Name of table
	_name = 'projects.employee'

	# Simple field of the object
	name = fields.Char(string='Nombre', required=True)
	nif = fields.Char(string='NIF', required=True)
	birthdate = fields.Date(string='Birthdate')
	gender = fields.Selection(string='Gender', selection=[('m','Male'),('f','Female')])
	address = fields.Char(string='Address')
	salary = fields.Float(string='Salary', default="300.0")
	christmas_extra = fields.Float(string='Christmas extra', default="200.0")
	total_earning = fields.Float(string='Total earning', compute='_compute_salary')
	director = fields.Selection(string="Director", selection=[('s','Yes'),('n','No')])
	color = fields.Integer()

	# Relational fields with other classes
	department_id = fields.Many2one('projects.department', string='Department')
	supervised_ids = fields.One2many('projects.employee', 'supervisor_id', string='Supervised')
	supervisor_id = fields.Many2one('projects.employee', string='Supervisor')
	project_ids = fields.Many2many('projects.project', string="Projects")

	# Function that calculates the total earnings in a year for an employee
	@api.multi
	def _compute_salary(self):
		for record in self:
			# Calculate using the christmas extra payment and the salary of a year
			record.total_earning = record.salary*12 + record.christmas_extra

	# Constraint of minimum and maximum salary for an employee
	@api.constrains('salario')
	def _check_salary(self):
		for record in self:
			if record.salary > 1500.0 or record.salary < 300.0:
				raise ValidationError("Salary is not valid, it has to be between 300 and 1500")

	# Override create function
	@api.model
	def create(self, values):
		# We create a new employee
		record = super(employees, self).create(values)
		# If the department of the employee has a director, then the employee cannot be a director
		if record.department_id.director_id:
			record['director'] = 'n'
		# If the department of the employee doesn't have a director, the employee is the director
		else:
			record['director'] = 's'

		# If the employee is the director, we save the relationship in the department information
		if record.director is 's':
			record.department_id.director_id = record
		return record