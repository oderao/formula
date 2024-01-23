frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        console.log("hello")
        frm.set_query('uom', 'items', function(doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                "filters": {
                    "item_code": d.item_code
                },
                query:"formula.utils.get_item_uom",
            };
        });
    }
})
