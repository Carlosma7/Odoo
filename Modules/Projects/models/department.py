# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Class for department management and their relationships
class Departments(models.Model):
	# Name of table
	_name = 'projects.department'

	# Simple fields of the object
	name = fields.Char(string="Department", required=True)
	number = fields.Integer(string="ID", required=True)
	member_number = fields.Integer(string="Number of members", compute="_total_employees", store=True)
	project_number = fields.Integer(string="Number of projects", compute="_total_projects", store=True)

	# Relational fields with other classes
	director_id = fields.Many2one('projects.employee', string="Director")
	member_ids = fields.One2many('projects.employee','department_id', string="Members", domain=[('salary','<=','1500.0'),('salary','>=','300.0')])
	project_ids = fields.One2many('projects.project', 'department_ids', string="Projects")

	# Function that calculates the number of employees in a department to save them into a field
	@api.depends('member_ids')
	@api.multi
	def _total_employees(self):
		for record in self:
			if record.member_ids:
				record.member_number = len(record.member_ids)

	# Function that calculates the number of projects in a department to save them into a field
	@api.depends('project_ids')
	@api.multi
	def _total_projects(self):
		for record in self:
			if record.project_ids:
				record.project_number = len(record.project_ids)