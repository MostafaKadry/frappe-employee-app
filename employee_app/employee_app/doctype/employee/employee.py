# Copyright (c) 2025, Mostafa K. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class Employee(Document):
    def validate(self):
        # auto calculate employed_days.
        self.auto_calc_employed_days()

        # Ensure department-company alignment and prevent manual edits to certain fields.
        if self.department:
            dept_company = frappe.db.get_value("Department", self.department, "company")
            if dept_company and dept_company != self.company:
                frappe.log_error(
                    f"Department {self.department} belongs to company {dept_company}, not {self.company}.",
                    "Invalid Department-Company Link"
                )
                frappe.response["message"]=(
                    f"Department {self.department} belongs to company {dept_company}, not {self.company}."
                )
                frappe.response["http_status_code"] = 400

                return

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
            frappe.db.commit()

        except Exception:
            frappe.throw( f"Failed to update employee count for department {self.department} and company {self.company}")



    def auto_calc_employed_days(self):
        if self.status != "Hired" or not self.hired_on:
            return
        else:
            hire_date = getdate(self.hired_on)
            today = getdate(nowdate())
		
        if hire_date > today:
            frappe.throw("Hire date cannot be in the future", exc=frappe.ValidationError)
			
        self.employed_days = (today - hire_date).days
