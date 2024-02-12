import frappe
from erpnext.stock.utils import get_stock_balance


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

@frappe.whitelist()
def get_warehouse_and_rate(item,uom,customer):
	if item and uom:
		warehouse = frappe.db.get_value("UOM Conversion Detail",{"parent":item,"uom":uom},"custom_warehouse")
		
		uom_rate = frappe.db.get_value("UOM Conversion Detail",{"parent":item,"uom":uom},"custom_uom_rate")
		
		#get discounted_rate if item in discount group
		if frappe.db.exists("Discount Group Customer",{"customer":customer}):
			discount_parent = frappe.db.get_value("Discount Group Customer",{"customer":customer},"parent")
			if discount_parent:
				if frappe.db.exists("Discount Group Item Table",{"parent":discount_parent,"item":item}):
					percentage_discount = frappe.db.get_value("Discount Group",discount_parent,"discount")
					uom_rate = uom_rate - ((percentage_discount / 100) * uom_rate)
		qty = frappe.db.get_value("UOM Conversion Detail",{"parent":item,"uom":uom},"custom_minimum_qty")
		
		return {"uom_rate":uom_rate,"warehouse":warehouse,"qty":qty}

@frappe.whitelist()
def get_uom_list(item):
	if item:
		uom_list = frappe.get_list("UOM Conversion Detail",{"parent":item},["uom","custom_uom_rate","custom_warehouse"])
		
		return [i["uom"] + "/" + frappe.utils.fmt_money(i["custom_uom_rate"],currency="ZAR") + "/" + str(get_stock_balance(item,i["custom_warehouse"]))  for i in uom_list]
	
@frappe.whitelist()
def get_converted_rate_and_qty(item,qty,convert_from,convert_to):
	if item:
		convert_from = convert_from.split("/")[0]
		convert_to = convert_to.split("/")[0]
		
		convert_from = frappe.get_doc("UOM Conversion Detail",{"parent":item,"uom":convert_from})
		convert_to = frappe.get_doc("UOM Conversion Detail",{"parent":item,"uom":convert_to})
		
		convert_from_rate = convert_from.custom_uom_rate
		convert_to_rate = convert_to.custom_uom_rate
		
		convert_from_factor = convert_from.custom_conversion_factor #conversion factor
		convert_to_factor= convert_to.custom_conversion_factor
		
		
		conversion_rate =  convert_to_rate/convert_from_rate
		
		convert_to_minimum_qty = convert_to.custom_minimum_qty
		
		conversion_factor = convert_to_factor/convert_from_factor
		
		converted_qty = float(conversion_factor) * float(qty)
		amount_to_sell_at = (float(converted_qty) * convert_to_rate)/convert_to_minimum_qty
		
		converted_rate = amount_to_sell_at
		
		return {"converted_rate":converted_rate,"converted_qty":converted_qty}

@frappe.whitelist()
def get_html_for_stock_balance(item):
	
	html_template = """<!DOCTYPE html>
	<html>
	<head>
	<style>
	table {
	font-family: arial, sans-serif;
	border-collapse: collapse;
	width: 100%;
	}

	td, th {
	border: 1px solid #dddddd;
	text-align: left;
	padding: 8px;
	}

	tr:nth-child(even) {
	background-color: #dddddd;
	}
	</style>
	</head>
	<body>
	<div class="uom_table">
	<h2>Item Stock Balance</h2>

	<table>
	<tr>
		<th>UOM</th>
		<th>Warehouse</th>
		<th>Stock Balance</th>
	</tr>
	{% for uom in uoms %}
		<tr>
			<td>{{uom["uom"]}}</td>
			<td>{{uom["custom_warehouse"]}}</td>
			<td>{{uom["stock_balance"]}}</td>
		</tr>
	{% endfor %}
	
	</table>
	<div>
	</body>
	</html>"""
	
	uom_list = frappe.get_all("UOM Conversion Detail",{"parent":item},["uom","custom_uom_rate","custom_warehouse"])
	for i in uom_list:
		i["stock_balance"] = str(get_stock_balance(item,i["custom_warehouse"])) 
  
	contxt_dict = {"uoms":uom_list}
	return frappe.render_template(html_template,contxt_dict)
 