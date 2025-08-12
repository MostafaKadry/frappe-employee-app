# Copyright (c) 2025, Mostafa K. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
    def validate(self):
        """Ensure department-company alignment and prevent manual edits to certain fields."""
        if self.department:
            dept_company = frappe.db.get_value("Department", self.department, "company")
            if dept_company and dept_company != self.company:
                frappe.log_error(
                    f"Department {self.department} belongs to company {dept_company}, not {self.company}.",
                    "Invalid Department-Company Link"
                )
                frappe.throw(
                    f"Department {self.department} belongs to company {dept_company}, not {self.company}."
                )

        # Prevent manual changes to system-controlled fields
        restricted_fields = {
            "status": "Status cannot be set manually. It is automatically updated based on employment status.",
            "hired_on": "Hired On date cannot be set manually. It is automatically set to the current date when the employee is hired.",
            "days_employed": "Days Employed cannot be set manually. It is automatically calculated based on the Hired On date."
        }

        # for field, message in restricted_fields.items():
        #     if self.has_value_changed(field):
        #         frappe.throw(message)


    def after_insert(self):
        self.update_employee_count()

    def on_update(self):
        self.update_employee_count()

    def on_trash(self):
        self.update_employee_count()

    def update_employee_count(self):
        """Update number_of_employees for related Department and Company."""
		
        if not self.department:
            frappe.throw("Employee must be linked to a department to update employee count.")

        if not self.company:
            frappe.throw("Employee must be linked to a company to update employee count.")

        try:
            # Count employees in department and company
            employees_in_department_count = frappe.db.count("Employee", {"department": self.department})
            employees_in_company_count = frappe.db.count("Employee", {"company": self.company})

            # Update both records
            frappe.db.set_value("Department", self.department, "number_of_employees", employees_in_department_count)
            frappe.db.set_value("Company", self.company, "number_of_employees", employees_in_company_count)

        except Exception:
            frappe.throw( f"Failed to update employee count for department {self.department} and company {self.company}")


