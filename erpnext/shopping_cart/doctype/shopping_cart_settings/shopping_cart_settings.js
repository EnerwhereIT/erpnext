// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Shopping Cart Settings", {
	onload: function(frm) {
		if(frm.doc.__onload && frm.doc.__onload.quotation_series) {
			frm.fields_dict.quotation_series.df.options = frm.doc.__onload.quotation_series;
			frm.refresh_field("quotation_series");
		}

		frm.set_query('payment_gateway_account', function() {
			return { 'filters': { 'payment_channel': "Email" } };
		});
	},
<<<<<<< HEAD
	refresh: function(frm){
		toggle_mandatory(frm)
	},
	enable_checkout: function(frm){
		toggle_mandatory(frm)
	},
=======
	refresh: function(frm) {
		if (frm.doc.enabled) {
			frm.get_field('store_page_docs').$wrapper.removeClass('hide-control').html(
				`<div>${__("Follow these steps to create a landing page for your store")}:
					<a href="https://docs.erpnext.com/docs/user/manual/en/website/store-landing-page"
						style="color: var(--gray-600)">
						docs/store-landing-page
					</a>
				</div>`
			);
		}
	},
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
	enabled: function(frm) {
		if (frm.doc.enabled === 1) {
			frm.set_value('enable_variants', 1);
		}
<<<<<<< HEAD
		let is_required = frm.doc.enabled ? 1 : 0;
		frm.toggle_reqd(["company", "default_customer_group", "quotation_series"], is_required);
	}
});


function toggle_mandatory (frm){
	frm.toggle_reqd("payment_gateway_account", false);
	if(frm.doc.enabled && frm.doc.enable_checkout) {
		frm.toggle_reqd("payment_gateway_account", true);
	}
}
=======
		else {
			frm.set_value('company', '');
			frm.set_value('price_list', '');
			frm.set_value('default_customer_group', '');
			frm.set_value('quotation_series', '');
		}
	}
});
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
