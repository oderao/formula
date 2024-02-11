frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        frm.set_query('uom', 'items', function(doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                "filters": {
                    "item_code": d.item_code
                },
                query:"formula.utils.get_item_uom",
            };
        });
    },
    custom_item_to_convert(frm){
        //get uom list 
        frm.set_value("custom_qty_to_convert", 0)

        frm.set_value("custom_converted_rate", 0)
        frm.set_value("custom_converted_qty", 0)

        frappe.call({
            method : "formula.utils.get_uom_list",
            args : {
                "item" : frm.doc.custom_item_to_convert
            },
            callback : function(r){
                console.log(r)
                if (r && r.message){
					cur_frm.set_df_property('custom_convert_from_uom',"options",r.message)
					cur_frm.set_df_property('custom_convert_to_uom',"options",r.message)
                    frm.refresh_fields()

                }
            }
        })
    },
    custom_qty_to_convert(frm){
        if(frm.doc.custom_convert_from_uom && frm.doc.custom_convert_to_uom){
            frappe.call({
                method:"formula.utils.get_converted_rate_and_qty",
                args:{
                    "item": frm.doc.custom_item_to_convert,
                    "qty" : frm.doc.custom_qty_to_convert,
                    "convert_from" : frm.doc.custom_convert_from_uom,
                    "convert_to" : frm.doc.custom_convert_to_uom
                },
                callback:function(r){
                    frm.set_value("custom_converted_rate", r.message.converted_rate)
                    frm.set_value("custom_converted_qty",r.message.converted_qty)
                    frm.refresh_fields()
                }
            })
        }
        
    },
    validate(frm){
        frm.set_value("custom_converted_rate", "")
        frm.set_value("custom_converted_qty","")
        frm.set_value("custom_item_to_convert", "")
        frm.set_value("custom_qty_to_convert",0)
    }
})


frappe.ui.form.on('Sales Invoice Item', {
    // cdt is Child DocType name i.e Sales Invoice Item
    // cdn is the row name for e.g bbfcb8da6a
    uom(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        // get item warehouse and rate by unit of measure
        frappe.call({
            method:"formula.utils.get_warehouse_and_rate",
            args:{
                "uom":row.uom,
                "item":row.item_name
            },
            callback:function(r){
                row.warehouse = r.message.warehouse
                row.rate = r.message.uom_rate
                row.base_rate = r.message.uom_rate
                row.price_list_rate = r.message.uom_rate
                row.base_price_list_rate = r.message.uom_rate
                row.qty = r.message.qty
                // row.amount = r.message.uom_rate * row.qty
                // row.base_amount = r.message.uom_rate * row.qty
                cur_frm.refresh_field("items")
                //cur_frm.refresh_fields()
                //cur_frm.cscript.calculate_taxes_and_totals();


            }

        })
        //add discount percentage
    },
    item_code(frm,cdt,cdn){
        let row = frappe.get_doc(cdt, cdn);
        
        var stock_balance_wrapper = frm.fields_dict.custom_item_stock_balance.wrapper
        $(stock_balance_wrapper).html("")
        console.log("yessss")
        frappe.call({
            method:"formula.utils.get_html_for_stock_balance",
            args:{
                "item": row.item_code,
            },
            callback:function(r){
                if (r.message){
                    $(r.message).appendTo(stock_balance_wrapper);
                    
                }
            }
        })
        
    }
})

