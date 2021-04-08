frappe.provide('erpnext.accounts');

<<<<<<< HEAD
let default_dimensions = {};

let doctypes_with_dimensions = ["GL Entry", "Sales Invoice", "Purchase Invoice", "Payment Entry", "Asset",
	"Expense Claim", "Stock Entry", "Budget", "Payroll Entry", "Delivery Note", "Shipping Rule", "Loyalty Program",
	"Fee Schedule", "Fee Structure", "Stock Reconciliation", "Travel Request", "Fees", "POS Profile", "Opening Invoice Creation Tool",
	"Subscription", "Purchase Order", "Journal Entry", "Material Request", "Purchase Receipt", "Landed Cost Item", "Asset"];

let child_docs = ["Sales Invoice Item", "Purchase Invoice Item", "Purchase Order Item", "Journal Entry Account",
	"Material Request Item", "Delivery Note Item", "Purchase Receipt Item", "Stock Entry Detail", "Payment Entry Deduction",
	"Landed Cost Item", "Asset Value Adjustment", "Opening Invoice Creation Tool Item", "Subscription Plan"];

frappe.call({
	method: "erpnext.accounts.doctype.accounting_dimension.accounting_dimension.get_dimension_filters",
	callback: function(r) {
		erpnext.dimension_filters = r.message[0];
		default_dimensions = r.message[1];
	}
});

doctypes_with_dimensions.forEach((doctype) => {
	frappe.ui.form.on(doctype, {
		onload: function(frm) {
			erpnext.dimension_filters.forEach((dimension) => {
				frappe.model.with_doctype(dimension['document_type'], () => {
					if(frappe.meta.has_field(dimension['document_type'], 'is_group')) {
						frm.set_query(dimension['fieldname'], {
							"is_group": 0
						});
					}
=======
erpnext.accounts.dimensions = {
	setup_dimension_filters(frm, doctype) {
		this.accounting_dimensions = [];
		this.default_dimensions = {};
		this.fetch_custom_dimensions(frm, doctype);
	},

	fetch_custom_dimensions(frm, doctype) {
		let me = this;
		frappe.call({
			method: "erpnext.accounts.doctype.accounting_dimension.accounting_dimension.get_dimensions",
			args: {
				'with_cost_center_and_project': true
			},
			callback: function(r) {
				me.accounting_dimensions = r.message[0];
				me.default_dimensions = r.message[1];
				me.setup_filters(frm, doctype);
			}
		});
	},

	setup_filters(frm, doctype) {
		if (this.accounting_dimensions) {
			this.accounting_dimensions.forEach((dimension) => {
				frappe.model.with_doctype(dimension['document_type'], () => {
					let parent_fields = [];
					frappe.meta.get_docfields(doctype).forEach((df) => {
						if (df.fieldtype === 'Link' && df.options === 'Account') {
							parent_fields.push(df.fieldname);
						} else if (df.fieldtype === 'Table') {
							this.setup_child_filters(frm, df.options, df.fieldname, dimension['fieldname']);
						}

						if (frappe.meta.has_field(doctype, dimension['fieldname'])) {
							this.setup_account_filters(frm, dimension['fieldname'], parent_fields);
						}
					});
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
				});
			});
		}
	},

	setup_child_filters(frm, doctype, parentfield, dimension) {
		let fields = [];

<<<<<<< HEAD
		company: function(frm) {
			if(frm.doc.company && (Object.keys(default_dimensions || {}).length > 0)
				&& default_dimensions[frm.doc.company]) {
				frm.trigger('update_dimension');
			}
		},

		update_dimension: function(frm) {
			erpnext.dimension_filters.forEach((dimension) => {
				if(frm.is_new()) {
					if(frm.doc.company && Object.keys(default_dimensions || {}).length > 0
						&& default_dimensions[frm.doc.company]) {

						let default_dimension = default_dimensions[frm.doc.company][dimension['fieldname']];

						if(default_dimension) {
							if (frappe.meta.has_field(doctype, dimension['fieldname'])) {
								frm.set_value(dimension['fieldname'], default_dimension);
							}

=======
		if (frappe.meta.has_field(doctype, dimension)) {
			frappe.model.with_doctype(doctype, () => {
				frappe.meta.get_docfields(doctype).forEach((df) => {
					if (df.fieldtype === 'Link' && df.options === 'Account') {
						fields.push(df.fieldname);
					}
				});

				frm.set_query(dimension, parentfield, function(doc, cdt, cdn) {
					let row = locals[cdt][cdn];
					return erpnext.queries.get_filtered_dimensions(row, fields, dimension, doc.company);
				});
			});
		}
	},

	setup_account_filters(frm, dimension, fields) {
		frm.set_query(dimension, function(doc) {
			return erpnext.queries.get_filtered_dimensions(doc, fields, dimension, doc.company);
		});
	},

	update_dimension(frm, doctype) {
		if (this.accounting_dimensions) {
			this.accounting_dimensions.forEach((dimension) => {
				if (frm.is_new()) {
					if (frm.doc.company && Object.keys(this.default_dimensions || {}).length > 0
						&& this.default_dimensions[frm.doc.company]) {

						let default_dimension = this.default_dimensions[frm.doc.company][dimension['fieldname']];

						if (default_dimension) {
							if (frappe.meta.has_field(doctype, dimension['fieldname'])) {
								frm.set_value(dimension['fieldname'], default_dimension);
							}

>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
							$.each(frm.doc.items || frm.doc.accounts || [], function(i, row) {
								frappe.model.set_value(row.doctype, row.name, dimension['fieldname'], default_dimension);
							});
						}
					}
				}
<<<<<<< HEAD
			});
		}
	});
});

child_docs.forEach((doctype) => {
	frappe.ui.form.on(doctype, {
		items_add: function(frm, cdt, cdn) {
			erpnext.dimension_filters.forEach((dimension) => {
				var row = frappe.get_doc(cdt, cdn);
				frm.script_manager.copy_from_first_row("items", row, [dimension['fieldname']]);
=======
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
			});
		}
	},

	copy_dimension_from_first_row(frm, cdt, cdn, fieldname) {
		if (frappe.meta.has_field(frm.doctype, fieldname) && this.accounting_dimensions) {
			this.accounting_dimensions.forEach((dimension) => {
				let row = frappe.get_doc(cdt, cdn);
				frm.script_manager.copy_from_first_row(fieldname, row, [dimension['fieldname']]);
			});
		}
	}
};