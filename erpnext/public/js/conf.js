// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide('erpnext');

// preferred modules for breadcrumbs
$.extend(frappe.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	"Territory": "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
<<<<<<< HEAD
	"Brand": "Stock"
=======
	"Brand": "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support"
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
});

$.extend(frappe.breadcrumbs.module_map, {
	'ERPNext Integrations': 'Integrations',
	'Geo': 'Settings',
	'Portal': 'Website',
	'Utilities': 'Settings',
	'Shopping Cart': 'Website',
	'Contacts': 'CRM'
});
