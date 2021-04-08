# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate
from erpnext.accounts.utils import get_fiscal_year

class TaxWithholdingCategory(Document):
	pass

<<<<<<< HEAD
def get_party_tax_withholding_details(ref_doc, tax_withholding_category=None):

	pan_no = ''
	suppliers = []

	if not tax_withholding_category:
		tax_withholding_category, pan_no = frappe.db.get_value('Supplier', ref_doc.supplier, ['tax_withholding_category', 'pan'])
=======
def get_party_details(inv):
	party_type, party = '', ''

	if inv.doctype == 'Sales Invoice':
		party_type = 'Customer'
		party = inv.customer
	else:
		party_type = 'Supplier'
		party = inv.supplier
	
	return party_type, party

def get_party_tax_withholding_details(inv, tax_withholding_category=None):
	pan_no = ''
	parties = []
	party_type, party = get_party_details(inv)

	if not tax_withholding_category:
		tax_withholding_category, pan_no = frappe.db.get_value(party_type, party, ['tax_withholding_category', 'pan'])
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

	if not tax_withholding_category:
		return

<<<<<<< HEAD
	if not pan_no:
		pan_no = frappe.db.get_value('Supplier', ref_doc.supplier, 'pan')

	# Get others suppliers with the same PAN No
	if pan_no:
		suppliers = [d.name for d in  frappe.get_all('Supplier', fields=['name'], filters={'pan': pan_no})]

	if not suppliers:
		suppliers.append(ref_doc.supplier)

	fy = get_fiscal_year(ref_doc.posting_date, company=ref_doc.company)
	tax_details = get_tax_withholding_details(tax_withholding_category, fy[0], ref_doc.company)
	if not tax_details:
		frappe.throw(_('Please set associated account in Tax Withholding Category {0} against Company {1}')
			.format(tax_withholding_category, ref_doc.company))

	tds_amount = get_tds_amount(suppliers, ref_doc.net_total, ref_doc.company,
		tax_details, fy,  ref_doc.posting_date, pan_no)

	tax_row = get_tax_row(tax_details, tds_amount)
=======
	# if tax_withholding_category passed as an argument but not pan_no
	if not pan_no:
		pan_no = frappe.db.get_value(party_type, party, 'pan')

	# Get others suppliers with the same PAN No
	if pan_no:
		parties = frappe.get_all(party_type, filters={ 'pan': pan_no }, pluck='name')

	if not parties:
		parties.append(party)

	fiscal_year = get_fiscal_year(inv.posting_date, company=inv.company)
	tax_details = get_tax_withholding_details(tax_withholding_category, fiscal_year[0], inv.company)

	if not tax_details:
		frappe.throw(_('Please set associated account in Tax Withholding Category {0} against Company {1}')
			.format(tax_withholding_category, inv.company))

	if party_type == 'Customer' and not tax_details.cumulative_threshold:
		# TCS is only chargeable on sum of invoiced value
		frappe.throw(_('Tax Withholding Category {} against Company {} for Customer {} should have Cumulative Threshold value.')
			.format(tax_withholding_category, inv.company, party))

	tax_amount, tax_deducted = get_tax_amount(
		party_type, parties,
		inv, tax_details,
		fiscal_year, pan_no
	)

	if party_type == 'Supplier':
		tax_row = get_tax_row_for_tds(tax_details, tax_amount)
	else:
		tax_row = get_tax_row_for_tcs(inv, tax_details, tax_amount, tax_deducted)
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

	return tax_row

def get_tax_withholding_details(tax_withholding_category, fiscal_year, company):
	tax_withholding = frappe.get_doc("Tax Withholding Category", tax_withholding_category)

	tax_rate_detail = get_tax_withholding_rates(tax_withholding, fiscal_year)

	for account_detail in tax_withholding.accounts:
		if company == account_detail.company:
			return frappe._dict({
				"account_head": account_detail.account,
				"rate": tax_rate_detail.tax_withholding_rate,
				"threshold": tax_rate_detail.single_threshold,
				"cumulative_threshold": tax_rate_detail.cumulative_threshold,
				"description": tax_withholding.category_name if tax_withholding.category_name else tax_withholding_category
			})

def get_tax_withholding_rates(tax_withholding, fiscal_year):
	# returns the row that matches with the fiscal year from posting date
	for rate in tax_withholding.rates:
		if rate.fiscal_year == fiscal_year:
			return rate

	frappe.throw(_("No Tax Withholding data found for the current Fiscal Year."))

<<<<<<< HEAD
def get_tax_row(tax_details, tds_amount):

=======
def get_tax_row_for_tcs(inv, tax_details, tax_amount, tax_deducted):
	row = {
		"category": "Total",
		"charge_type": "Actual",
		"tax_amount": tax_amount,
		"description": tax_details.description,
		"account_head": tax_details.account_head
	}

	if tax_deducted:
		# TCS already deducted on previous invoices
		# So, TCS will be calculated by 'Previous Row Total'

		taxes_excluding_tcs = [d for d in inv.taxes if d.account_head != tax_details.account_head]
		if taxes_excluding_tcs:
			# chargeable amount is the total amount after other charges are applied
			row.update({
				"charge_type": "On Previous Row Total",
				"row_id": len(taxes_excluding_tcs),
				"rate": tax_details.rate
			})
		else:
			# if only TCS is to be charged, then net total is chargeable amount
			row.update({
				"charge_type": "On Net Total",
				"rate": tax_details.rate
			})

	return row

def get_tax_row_for_tds(tax_details, tax_amount):
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
	return {
		"category": "Total",
		"charge_type": "Actual",
		"tax_amount": tax_amount,
		"add_deduct_tax": "Deduct",
		"description": tax_details.description,
		"account_head": tax_details.account_head
	}

<<<<<<< HEAD
def get_tds_amount(suppliers, net_total, company, tax_details, fiscal_year_details, posting_date, pan_no=None):
	fiscal_year, year_start_date, year_end_date = fiscal_year_details
=======
def get_lower_deduction_certificate(fiscal_year, pan_no):
	ldc_name = frappe.db.get_value('Lower Deduction Certificate', { 'pan_no': pan_no, 'fiscal_year': fiscal_year }, 'name')
	if ldc_name:
		return frappe.get_doc('Lower Deduction Certificate', ldc_name)

def get_tax_amount(party_type, parties, inv, tax_details, fiscal_year_details, pan_no=None):
	fiscal_year = fiscal_year_details[0]

	vouchers = get_invoice_vouchers(parties, fiscal_year, inv.company, party_type=party_type)
	advance_vouchers = get_advance_vouchers(parties, fiscal_year, inv.company, party_type=party_type)
	taxable_vouchers = vouchers + advance_vouchers

	tax_deducted = 0
	if taxable_vouchers:
		tax_deducted = get_deducted_tax(taxable_vouchers, fiscal_year, tax_details)

	tax_amount = 0
	posting_date = inv.posting_date
	if party_type == 'Supplier':
		ldc = get_lower_deduction_certificate(fiscal_year, pan_no)
		if tax_deducted:
			net_total = inv.net_total
			if ldc:
				tax_amount = get_tds_amount_from_ldc(ldc, parties, fiscal_year, pan_no, tax_details, posting_date, net_total)
			else:
				tax_amount = net_total * tax_details.rate / 100 if net_total > 0 else 0
		else:
			tax_amount = get_tds_amount(
				ldc, parties, inv, tax_details,
				fiscal_year_details, tax_deducted, vouchers
			)

	elif party_type == 'Customer':
		if tax_deducted:
			# if already TCS is charged, then amount will be calculated based on 'Previous Row Total'
			tax_amount = 0
		else:
			#  if no TCS has been charged in FY,
			# then chargeable value is "prev invoices + advances" value which cross the threshold
			tax_amount = get_tcs_amount(
				parties, inv, tax_details,
				fiscal_year_details, vouchers, advance_vouchers
			)

	return tax_amount, tax_deducted

def get_invoice_vouchers(parties, fiscal_year, company, party_type='Supplier'):
	dr_or_cr = 'credit' if party_type == 'Supplier' else 'debit'

	filters = {
		dr_or_cr: ['>', 0],
		'company': company,
		'party_type': party_type,
		'party': ['in', parties],
		'fiscal_year': fiscal_year,
		'is_opening': 'No',
		'is_cancelled': 0
	}

	return frappe.get_all('GL Entry', filters=filters, distinct=1, pluck="voucher_no") or [""]

def get_advance_vouchers(parties, fiscal_year=None, company=None, from_date=None, to_date=None, party_type='Supplier'):
	# for advance vouchers, debit and credit is reversed
	dr_or_cr = 'debit' if party_type == 'Supplier' else 'credit'

	filters = {
		dr_or_cr: ['>', 0],
		'is_opening': 'No',
		'is_cancelled': 0,
		'party_type': party_type,
		'party': ['in', parties],
		'against_voucher': ['is', 'not set']
	}

	if fiscal_year:
		filters['fiscal_year'] = fiscal_year
	if company:
		filters['company'] = company
	if from_date and to_date:
		filters['posting_date'] = ['between', (from_date, to_date)]

	return frappe.get_all('GL Entry', filters=filters, distinct=1, pluck='voucher_no') or [""]

def get_deducted_tax(taxable_vouchers, fiscal_year, tax_details):
	# check if TDS / TCS account is already charged on taxable vouchers
	filters = {
		'is_cancelled': 0,
		'credit': ['>', 0],
		'fiscal_year': fiscal_year,
		'account': tax_details.account_head,
		'voucher_no': ['in', taxable_vouchers],
	}
	field = "sum(credit)"

	return frappe.db.get_value('GL Entry', filters, field) or 0.0

def get_tds_amount(ldc, parties, inv, tax_details, fiscal_year_details, tax_deducted, vouchers):
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
	tds_amount = 0

<<<<<<< HEAD
	def _get_tds(amount, rate):
		if amount <= 0:
			return 0

		return amount * rate / 100

	ldc_name = frappe.db.get_value('Lower Deduction Certificate',
		{
			'pan_no': pan_no,
			'fiscal_year': fiscal_year
		}, 'name')
	ldc = ''

	if ldc_name:
		ldc = frappe.get_doc('Lower Deduction Certificate', ldc_name)

	entries = frappe.db.sql("""
			select voucher_no, credit
			from `tabGL Entry`
			where company = %s and
			party in %s and fiscal_year=%s and credit > 0
			and is_opening = 'No'
		""", (company, tuple(suppliers), fiscal_year), as_dict=1)

	vouchers = [d.voucher_no for d in entries]
	advance_vouchers = get_advance_vouchers(suppliers, fiscal_year=fiscal_year, company=company)
=======
	supp_credit_amt = frappe.db.get_value('Purchase Invoice', {
		'name': ('in', vouchers), 'docstatus': 1, 'apply_tds': 1
	}, 'sum(net_total)') or 0.0

	supp_jv_credit_amt = frappe.db.get_value('Journal Entry Account', {
		'parent': ('in', vouchers), 'docstatus': 1,
		'party': ('in', parties), 'reference_type': ('!=', 'Purchase Invoice')
	}, 'sum(credit_in_account_currency)') or 0.0

	supp_credit_amt += supp_jv_credit_amt
	supp_credit_amt += inv.net_total

	debit_note_amount = get_debit_note_amount(parties, fiscal_year_details, inv.company)
	supp_credit_amt -= debit_note_amount
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

	threshold = tax_details.get('threshold', 0)
	cumulative_threshold = tax_details.get('cumulative_threshold', 0)

	if ((threshold and supp_credit_amt >= threshold) or (cumulative_threshold and supp_credit_amt >= cumulative_threshold)):
		if ldc and is_valid_certificate(
			ldc.valid_from, ldc.valid_upto,
			inv.posting_date, tax_deducted,
			inv.net_total, ldc.certificate_limit
		):
			tds_amount = get_ltds_amount(supp_credit_amt, 0, ldc.certificate_limit, ldc.rate, tax_details)
		else:
			tds_amount = supp_credit_amt * tax_details.rate / 100 if supp_credit_amt > 0 else 0

	return tds_amount

<<<<<<< HEAD
	if tds_deducted:
		if ldc:
			limit_consumed = frappe.db.get_value('Purchase Invoice',
				{
					'supplier': ('in', suppliers),
					'apply_tds': 1,
					'docstatus': 1
				}, 'sum(net_total)')

		if ldc and is_valid_certificate(ldc.valid_from, ldc.valid_upto, posting_date, limit_consumed, net_total,
			ldc.certificate_limit):

			tds_amount = get_ltds_amount(net_total, limit_consumed, ldc.certificate_limit, ldc.rate, tax_details)
		else:
			tds_amount = _get_tds(net_total, tax_details.rate)
	else:
		supplier_credit_amount = frappe.get_all('Purchase Invoice',
			fields = ['sum(net_total)'],
			filters = {'name': ('in', vouchers), 'docstatus': 1, "apply_tds": 1}, as_list=1)
=======
def get_tcs_amount(parties, inv, tax_details, fiscal_year_details, vouchers, adv_vouchers):
	tcs_amount = 0
	fiscal_year, _, _ = fiscal_year_details

	# sum of debit entries made from sales invoices
	invoiced_amt = frappe.db.get_value('GL Entry', {
		'is_cancelled': 0,
		'party': ['in', parties],
		'company': inv.company,
		'voucher_no': ['in', vouchers],
	}, 'sum(debit)') or 0.0

	# sum of credit entries made from PE / JV with unset 'against voucher'
	advance_amt = frappe.db.get_value('GL Entry', {
		'is_cancelled': 0,
		'party': ['in', parties],
		'company': inv.company,
		'voucher_no': ['in', adv_vouchers],
	}, 'sum(credit)') or 0.0

	# sum of credit entries made from sales invoice
	credit_note_amt = frappe.db.get_value('GL Entry', {
		'is_cancelled': 0,
		'credit': ['>', 0],
		'party': ['in', parties],
		'fiscal_year': fiscal_year,
		'company': inv.company,
		'voucher_type': 'Sales Invoice',
	}, 'sum(credit)') or 0.0
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

	cumulative_threshold = tax_details.get('cumulative_threshold', 0)

<<<<<<< HEAD
		jv_supplier_credit_amt = frappe.get_all('Journal Entry Account',
			fields = ['sum(credit_in_account_currency)'],
			filters = {
				'parent': ('in', vouchers), 'docstatus': 1,
				'party': ('in', suppliers),
				'reference_type': ('not in', ['Purchase Invoice'])
			}, as_list=1)
=======
	current_invoice_total = get_invoice_total_without_tcs(inv, tax_details)
	total_invoiced_amt = current_invoice_total + invoiced_amt + advance_amt - credit_note_amt
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

	if ((cumulative_threshold and total_invoiced_amt >= cumulative_threshold)):
		chargeable_amt = total_invoiced_amt - cumulative_threshold
		tcs_amount = chargeable_amt * tax_details.rate / 100 if chargeable_amt > 0 else 0

<<<<<<< HEAD
		supplier_credit_amount += net_total

		debit_note_amount = get_debit_note_amount(suppliers, year_start_date, year_end_date)
		supplier_credit_amount -= debit_note_amount

		if ((tax_details.get('threshold', 0) and supplier_credit_amount >= tax_details.threshold)
			or (tax_details.get('cumulative_threshold', 0) and supplier_credit_amount >= tax_details.cumulative_threshold)):

			if ldc and is_valid_certificate(ldc.valid_from, ldc.valid_upto, posting_date, tds_deducted, net_total,
				ldc.certificate_limit):
				tds_amount = get_ltds_amount(supplier_credit_amount, 0, ldc.certificate_limit, ldc.rate,
					tax_details)
			else:
				tds_amount = _get_tds(supplier_credit_amount, tax_details.rate)
=======
	return tcs_amount

def get_invoice_total_without_tcs(inv, tax_details):
	tcs_tax_row = [d for d in inv.taxes if d.account_head == tax_details.account_head]
	tcs_tax_row_amount = tcs_tax_row[0].base_tax_amount if tcs_tax_row else 0

	return inv.grand_total - tcs_tax_row_amount
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

def get_tds_amount_from_ldc(ldc, parties, fiscal_year, pan_no, tax_details, posting_date, net_total):
	tds_amount = 0
	limit_consumed = frappe.db.get_value('Purchase Invoice', {
		'supplier': ('in', parties),
		'apply_tds': 1,
		'docstatus': 1
	}, 'sum(net_total)')

	if is_valid_certificate(
		ldc.valid_from, ldc.valid_upto,
		posting_date, limit_consumed,
		net_total, ldc.certificate_limit
	):
		tds_amount = get_ltds_amount(net_total, limit_consumed, ldc.certificate_limit, ldc.rate, tax_details)
	
	return tds_amount

<<<<<<< HEAD
def get_advance_vouchers(suppliers, fiscal_year=None, company=None, from_date=None, to_date=None):
	condition = "fiscal_year=%s" % fiscal_year

	if company:
		condition += "and company =%s" % (company)
	if from_date and to_date:
		condition += "and posting_date between %s and %s" % (from_date, to_date)

	## Appending the same supplier again if length of suppliers list is 1
	## since tuple of single element list contains None, For example ('Test Supplier 1', )
	## and the below query fails
	if len(suppliers) == 1:
		suppliers.append(suppliers[0])

	return frappe.db.sql_list("""
		select distinct voucher_no
		from `tabGL Entry`
		where party in %s and %s and debit > 0
		and is_opening = 'No'
	""", (tuple(suppliers), condition)) or []

def get_debit_note_amount(suppliers, year_start_date, year_end_date, company=None):
	condition = "and 1=1"
	if company:
		condition = " and company=%s " % company

	if len(suppliers) == 1:
		suppliers.append(suppliers[0])

	return flt(frappe.db.sql("""
		select abs(sum(net_total))
		from `tabPurchase Invoice`
		where supplier in %s and is_return=1 and docstatus=1
			and posting_date between %s and %s %s
	""", (tuple(suppliers), year_start_date, year_end_date, condition)))
=======
def get_debit_note_amount(suppliers, fiscal_year_details, company=None):
	_, year_start_date, year_end_date = fiscal_year_details

	filters = {
		'supplier': ['in', suppliers],
		'is_return': 1,
		'docstatus': 1,
		'posting_date': ['between', (year_start_date, year_end_date)]
	}
	fields = ['abs(sum(net_total)) as net_total']

	if company:
		filters['company'] = company

	return frappe.get_all('Purchase Invoice', filters, fields)[0].get('net_total') or 0.0
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

def get_ltds_amount(current_amount, deducted_amount, certificate_limit, rate, tax_details):
	if current_amount < (certificate_limit - deducted_amount):
		return current_amount * rate/100
	else:
		ltds_amount = (certificate_limit - deducted_amount)
		tds_amount = current_amount - ltds_amount

		return ltds_amount * rate/100 + tds_amount * tax_details.rate/100

def is_valid_certificate(valid_from, valid_upto, posting_date, deducted_amount, current_amount, certificate_limit):
	valid = False

	if ((getdate(valid_from) <= getdate(posting_date) <= getdate(valid_upto)) and
			certificate_limit > deducted_amount):
		valid = True

	return valid
