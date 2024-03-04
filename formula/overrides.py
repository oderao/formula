import frappe
from erpnext.stock.doctype.item.item import Item  


class CustomItem(Item):
     
    def add_default_uom_in_conversion_factor_table(self):
            if not self.is_new() and self.has_value_changed("stock_uom"):
                self.uoms = []
                frappe.msgprint(
                    _("Successfully changed Stock UOM, please redefine conversion factors for new UOM."),
                    alert=True,
                )

            uoms_list = [d.uom for d in self.get("uoms")]
            custom_uoms_list = [d.uom for d in self.get("custom_conversion_table")]
            if self.stock_uom not in uoms_list:
                self.append("uoms", {"uom": self.stock_uom, "conversion_factor": 1, "is_custom_default":1})
            
            if self.stock_uom not in custom_uoms_list:
                self.append("custom_conversion_table", {"uom": self.stock_uom, "conversion_factor": 1})