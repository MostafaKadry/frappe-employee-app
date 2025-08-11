# Copyright (c) 2025, Mostafa K. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Department(Document):
	pass


def update_employee_count(doc, method=None):
    if doc.department:
        count = frappe.db.count("Employee", {"department": doc.department})
        frappe.db.set_value("Department", doc.department, "number_of_employees", count)