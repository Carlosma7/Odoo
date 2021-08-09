#_*_ coding: utf-8 -*-
{
	'name': "Carlosma7",

	'summary': """
		This is the summary of the addon, second try.""",

	'description': """
		This is the description of the addon.
	""",

	'author': "Carlos Morales Aguilera",
	'website': "http://www.carlosma7.com",

	'category': 'Personal project',
	'version':'0.1',
	'application': True,

	'depends': ['base','sale','mail'],

	'data': [
		'data/data.xml',
		'security/ir.model.access.csv',
		'views/patient.xml',
		'views/kids.xml',
		'views/patient_gender.xml',
		'views/appointment.xml',
		'views/sale.xml',
		'views/doctor.xml',
		'wizard/create_appointment.xml'],

	'installable': True,
    'auto_install': True,
}
