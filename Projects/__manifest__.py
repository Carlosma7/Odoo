#_*_ coding: utf-8 -*-
{
	'name': "Project Management",

	'summary': """
		It allows to manage the projects to be carried out in a company and jobs.""",

	'description': """
		This module allows you to manage the projects of a company from departments, employees and projects.
	""",

	'author': "Carlos Morales Aguilera",
	'website': "http://www.example.com",

	'category': 'Personal project',
	'version':'0.1',
	'application': True,

	'depends': ['base'],

	'data': [
		'views/project.xml',
		'views/project_ext.xml',
		'views/department.xml',
		'views/employee.xml',
	],

	'installable': True,
    'auto_install': True,
}