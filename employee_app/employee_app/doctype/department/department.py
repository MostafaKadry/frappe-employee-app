# Copyright (c) 2025, Mostafa K.
# License information in license.txt

import frappe
from frappe.model.document import Document

class Department(Document):
    # --- Lifecycle Hooks ---
    def after_insert(self):
        """Triggered after a new department is inserted."""
        self._update_company_department_count()

    def on_update(self):
        """Triggered after department is updated."""
        self._update_company_department_count()
 
    def on_trash(self):
        """Triggered before department is deleted."""
        self._handle_related_records_before_delete()



    # --- Business Logic ---
    def _update_company_department_count(self):
        """Recalculate the number of departments for the linked company."""
        if not self.company:
            frappe.throw("Department must be linked to a company.")

        try:
            department_count = frappe.db.count("Department", {"company": self.company})
            frappe.db.set_value("Company", self.company, "number_of_departments", department_count)
        except Exception as e:
            frappe.log_error(message=str(e), title="Department Count Update Failed")
            frappe.throw(f"Could not update department count for company: {self.company}")

    def _handle_related_records_before_delete(self):
        """ Handle cascading deletions by delete related employees before department deletion. """
        related_employees = frappe.get_all(
            "Employee", filters={"department": self.name}, fields=["name"]
        )

        if related_employees:
            # cascade delete
            
            for emp in related_employees:
                frappe.delete_doc("Employee", emp.name, ignore_permissions=True)
            frappe.db.commit()
