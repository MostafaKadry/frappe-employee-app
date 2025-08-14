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
        frm.set_query("status", ()=>{
            if (frm.doc.status === "Hired" && !frm.doc.hired_on) {
                frm.set_value("hired_on", frappe.datetime.get_today());
            }
        })
        
	},
    
});
