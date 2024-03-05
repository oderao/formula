import frappe
from erpnext.stock.utils import get_stock_balance
import json

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
            discount_parent_enabled = frappe.db.get_value("Discount Group",discount_parent,"enabled")
            if discount_parent and discount_parent_enabled:
                if frappe.db.exists("Discount Group Item Table",{"parent":discount_parent,"item":item}):
                    default_percentage_discount = frappe.db.get_value("Discount Group",discount_parent,"discount")
                    percentage_discount = frappe.db.get_value("Discount Group Customer",{"customer":customer},"discount")
                    if not percentage_discount:
                        percentage_discount = default_percentage_discount or 0
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
def get_html_for_stock_balance(item,uom):

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
    <hr>

    <table>
    <tr>
        <th>UOM</th>

        <th>Converted Stock Balance</th>
    </tr>
    {% for uom in uoms %}
        <tr>
            <td>{{uom["uom"]}}</td>

            <td>{{uom["converted_stock_balance"]}}</td>
        </tr>
    {% endfor %}

    </table>
    <div>
    </body>
    </html>"""

    uom_list = frappe.get_all("UOM Conversion Detail",{"parent":item},["uom","custom_uom_rate","custom_warehouse","conversion_factor"])
    #get conversion factor for 
    conversion_factor = frappe.db.get_value("UOM Conversion Detail",{"parent":item,"uom":uom},"conversion_factor")
    for i in uom_list:
        if i["uom"] == uom:
            i["converted_stock_balance"] = get_stock_balance(item,i["custom_warehouse"])
        
        else:
            i["stock_balance"] = get_stock_balance(item,i["custom_warehouse"])
            i["converted_stock_balance"] = (i["stock_balance"] * conversion_factor)/i["conversion_factor"]
            #i["converted_stock_balance"] = i["stock_balance"] * i["conversion_factor"]
        
    contxt_dict = {"uoms":uom_list}
    return frappe.render_template(html_template,contxt_dict)



@frappe.whitelist()
def get_html_for_item_alternatives(item):

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
    text-align: right;
    padding: 8px;
    }

    tr:nth-child(even) {
    background-color: #dddddd;
    }
    </style>
    </head>
    <body>
    <div class="alter_table">
    <h2>Alternative Item</h2>
    <hr>

    <table>
    <tr>
        <th>Alternative Item</th>
        <th>Stock Balance Across All Warehouses</th>
    </tr>
    {% for item in items %}
        <tr>
            <td>{{item["item"]}}</td>

            <td>{{item["stock_balance"]}}</td>
        </tr>
    {% endfor %}

    </table>
    <div>
    </body>
    </html>"""

    item_list = frappe.get_all("Alternative Items",{"parent":item},["item"])
    if item_list:
        for i in item_list:
            warehouses = frappe.db.sql(f"""select warehouse from `tabStock Ledger Entry` where item_code = %s GROUP BY(warehouse)""",{i["item"]})
            if warehouses:
                warehouses = [element for tupl in warehouses for element in tupl]
                
                i["stock_balance"] = 0
                for warehouse in warehouses:
                    i["stock_balance"] += float(get_stock_balance(i["item"],warehouse))

        contxt_dict = {"items":item_list}
        return frappe.render_template(html_template,contxt_dict)

@frappe.whitelist()
def set_conversion_factors(items,parent,default_uom):

    #get default row
    if isinstance(items,str):
        items = json.loads(items)
    
    default_packing_qty = frappe.db.get_value("Item Conversion Table",{"parent":parent,"uom":default_uom},"packing_qty")
    #frappe.db.set_value("UOM Conversion Detail","a59dc42d9d","custom_conversion_factor",13)
    if default_packing_qty:
        for item in items:
            if item["uom"] == default_uom:
                # frappe.get_doc(item).save()
                frappe.db.set_value("UOM Conversion Detail",{"uom":item["uom"]},"conversion_factor",1)
                
                frappe.db.set_value("Item Conversion Table",item["name"],"conversion_factor",1)



            if item["packing_qty"] and item["uom"] != default_uom:
                custom_conversion_factor = default_packing_qty/item["packing_qty"]
                item["conversion_factor"] = custom_conversion_factor
                # frappe.get_doc(item).save()
                frappe.db.set_value("UOM Conversion Detail",{"uom":item["uom"]},"conversion_factor",custom_conversion_factor)
                
                frappe.db.set_value("Item Conversion Table",item["name"],"conversion_factor",custom_conversion_factor)
        frappe.db.commit()