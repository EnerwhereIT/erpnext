{% include "erpnext/regional/india/taxes.js" %}

erpnext.setup_auto_gst_taxation('Delivery Note');

<<<<<<< HEAD
=======
frappe.ui.form.on('Delivery Note', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && !frm.is_dirty() && !frm.doc.ewaybill) {
			frm.add_custom_button('E-Way Bill JSON', () => {
				frappe.call({
					method: 'erpnext.regional.india.utils.generate_ewb_json',
					args: {
						'dt': frm.doc.doctype,
						'dn': [frm.doc.name]
					},
					callback: function(r) {
						if (r.message) {
							const args = {
								cmd: 'erpnext.regional.india.utils.download_ewb_json',
								data: r.message,
								docname: frm.doc.name
							};
							open_url_post(frappe.request.url, args);
						}
					}
				});
			}, __("Create"));
		}
	}
})

>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
