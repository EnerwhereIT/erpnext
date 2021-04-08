frappe.query_reports["BOM Stock Report"] = {
	"filters": [
		{
			"fieldname": "bom",
			"label": __("BOM"),
			"fieldtype": "Link",
			"options": "BOM",
			"reqd": 1
		}, {
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"reqd": 1
		}, {
			"fieldname": "show_exploded_view",
			"label": __("Show exploded view"),
			"fieldtype": "Check"
		}, {
			"fieldname": "qty_to_produce",
			"label": __("Quantity to Produce"),
			"fieldtype": "Int",
			"default": "1"
		 },
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "item") {
			if (data["enough_parts_to_build"] > 0) {
<<<<<<< HEAD
				value = `<a style='color:green' href="#Form/Item/${data['item']}" data-doctype="Item">${data['item']}</a>`;
			} else {
				value = `<a style='color:red' href="#Form/Item/${data['item']}" data-doctype="Item">${data['item']}</a>`;
=======
				value = `<a style='color:green' href="/app/item/${data['item']}" data-doctype="Item">${data['item']}</a>`;
			} else {
				value = `<a style='color:red' href="/app/item/${data['item']}" data-doctype="Item">${data['item']}</a>`;
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
			}
		}
		return value
	}
}
