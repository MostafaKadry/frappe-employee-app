// Copyright (c) 2025, Mostafa K. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	refresh(frm) {
        frm.set_query("department", function() {
            return {
                filters: {
                    "company": frm.doc.company,
                }
            };
        });
        
	},
});
