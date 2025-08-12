# Copyright (c) 2025, Mostafa K. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Department(Document):

    # def validate(self):
    #     """Prevent manual editing of number_of_employees."""
    #     if self.has_value_changed("number_of_employees"):
    #         frappe.throw("Number of employees should not be set manually.")

    def after_insert(self):
        self.update_department_count()

    def on_update(self):
        self.update_department_count()

    def on_trash(self):
        self.update_department_count()

    def update_department_count(self):
        """Recalculate and update the number_of_departments for the related company."""
        if not self.company:
            frappe.throw("Department must be linked to a company to update department count.")

        try:
            count = frappe.db.count("Department", {"company": self.company})
            frappe.db.set_value("Company", self.company, "number_of_departments", count)
        except Exception as e:
            frappe.throw(f"Could not update department count for company {self.company}.")
