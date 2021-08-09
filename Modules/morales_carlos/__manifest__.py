#_*_ coding: utf-8 -*-
{
	'name': "morales_carlos",

	'summary': """
		New Odoo app for samll contact book.""",

	'description': """
		Your objective is to implement a small contact book whose contacts can be added manually through a form
(backend & frontend) or automatically through an XML file (a file upload for the user in the backend). You will be
assessed on the procedure, the correctness, the completeness and the promptness of your submission.
	""",

	'author': "Carlos Morales Aguilera",
	'website': "http://www.odoo.com",

	'category': 'Personal project',
	'version':'0.1',
	'application': True,

	'depends': ['base'],

	'data': [
		'data/data.xml',
		'security/ir.model.access.csv',
		'views/my_contact_view.xml',
		'wizards/xml_importer.xml'],

	'installable': True,
    'auto_install': True,
}
