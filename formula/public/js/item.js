frappe.ui.form.on("Item",{

    after_save(frm){
        //for validate
        frappe.call({
            method:"formula.utils.set_conversion_factors",
            args : {
                "items" :frm.doc.custom_conversion_table,
                "parent" : frm.doc.name,
                "default_uom" : frm.doc.stock_uom
            },
            callback:function(r){
                cur_frm.refresh_field("custom_conversion_table")
                cur_frm.refresh_fields()
                frm.reload_doc()

            }
        })
    }
})
frappe.ui.form.on('UOM Conversion Detail', {
    // cdt is Child DocType name i.
    // cdn is the row name for e.g bbfcb8da6a
   
    // custom_is_default(frm, cdt, cdn) {
    //         let default_uom = frm.doc.default_uom
    //         let row = frappe.get_doc(cdt, cdn);
    //         if (row.custom_is_default) {
    //             var uoms = frm.doc.uoms
    //             for (let index = 0; index < uoms.length; index++) {
    //                 var is_default = uoms[index]["custom_is_default"];
    //                 var uom = uoms[index]["uom"]
    //                 if (is_default && uom != default_uom){
    //                     frappe.msgprint("Ony default UOM can be set as default")
    //                     row.custom_is_default = 0
    //                     return false
    //                 } else {
    //                     // set conversion factor
                        
    //                 }
                   
    //             }

    //             // row.custom_conversion_factor = 1
    //             // for (let index = 0; index < uoms.length; index++) {
    //             //     reference_value = row.custom_packing_qty
                    
    //             //     const element = uoms[index];
                    
    //             // }
    //     }
        
    // }
    uom (frm,cdt,cdn){
        row = frappe.get_doc(cdt,cdn)
        // if (row.uom = frm.doc.default_uom){
        //     row.is_custom_default = 1
        // }
    }
   
        
    
})
