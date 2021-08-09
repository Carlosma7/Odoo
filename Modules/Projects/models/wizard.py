# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'projects.wizard'

    def _default_session(self):
        return self.env['projects.department'].browse(self._context.get('active_id'))

    department_id = fields.Many2one('projects.department', string="Department", required=True, default=_default_session)
    employee_ids = fields.Many2many('projects.employee', string="Employees")

    @api.multi
    def subscribe(self):
        self.department_id.member_ids |= self.employee_ids
        return {}