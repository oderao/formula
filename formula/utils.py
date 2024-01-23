import frappe


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_item_uom(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond
	query = """select uom from `tabUOM Conversion Detail`
				where uom like {txt}""".format(
			txt=frappe.db.escape("%{0}%".format(txt))
		)

	if filters and filters.get("item_code"):
		query += " and parent = {item_code}".format(item_code=frappe.db.escape(filters.get("item_code")))

	return frappe.db.sql(query, filters)

