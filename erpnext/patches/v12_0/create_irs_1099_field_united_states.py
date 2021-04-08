from __future__ import unicode_literals
import frappe
from erpnext.regional.united_states.setup import make_custom_fields

def execute():
<<<<<<< HEAD
    company = frappe.get_all('Company', filters = {'country': 'United States'})
    if not company:
        return

    make_custom_fields()
=======

	frappe.reload_doc('accounts', 'doctype', 'allowed_to_transact_with', force=True)
	frappe.reload_doc('accounts', 'doctype', 'pricing_rule_detail', force=True)
	frappe.reload_doc('crm', 'doctype', 'lost_reason_detail', force=True)
	frappe.reload_doc('setup', 'doctype', 'quotation_lost_reason_detail', force=True)

	company = frappe.get_all('Company', filters = {'country': 'United States'})
	if not company:
		return

	make_custom_fields()
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
