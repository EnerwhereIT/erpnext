erpnext.setup_auto_gst_taxation = (doctype) => {
	frappe.ui.form.on(doctype, {
		company_address: function(frm) {
			frm.trigger('get_tax_template');
		},
		shipping_address: function(frm) {
			frm.trigger('get_tax_template');
		},
<<<<<<< HEAD
=======
		supplier_address: function(frm) {
			frm.trigger('get_tax_template');
		},
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
		tax_category: function(frm) {
			frm.trigger('get_tax_template');
		},
		customer_address: function(frm) {
			frm.trigger('get_tax_template');
		},
		get_tax_template: function(frm) {
			if (!frm.doc.company) return;

			let party_details = {
				'shipping_address': frm.doc.shipping_address || '',
				'shipping_address_name': frm.doc.shipping_address_name || '',
				'customer_address': frm.doc.customer_address || '',
				'supplier_address': frm.doc.supplier_address,
				'customer': frm.doc.customer,
				'supplier': frm.doc.supplier,
				'supplier_gstin': frm.doc.supplier_gstin,
				'company_gstin': frm.doc.company_gstin,
				'tax_category': frm.doc.tax_category
			};

			frappe.call({
				method: 'erpnext.regional.india.utils.get_regional_address_details',
				args: {
					party_details: JSON.stringify(party_details),
					doctype: frm.doc.doctype,
					company: frm.doc.company
				},
<<<<<<< HEAD
				callback: function(r) {
					if(r.message) {
						frm.set_value('taxes_and_charges', r.message.taxes_and_charges);
						frm.set_value('place_of_supply', r.message.place_of_supply);
					} else if (frm.doc.is_internal_supplier || frm.doc.is_internal_customer) {
						frm.set_value('taxes_and_charges', '');
						frm.set_value('taxes', []);
=======
				debounce: 2000,
				callback: function(r) {
					if(r.message) {
						frm.set_value('taxes_and_charges', r.message.taxes_and_charges);
						frm.set_value('taxes', r.message.taxes);
						frm.set_value('place_of_supply', r.message.place_of_supply);
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
					}
				}
			});
		}
	});
<<<<<<< HEAD
};
=======
}
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a

