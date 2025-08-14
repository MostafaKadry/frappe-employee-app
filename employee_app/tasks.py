import frappe
from frappe.utils import today, getdate

# hook to update days employed for all employees
def update_days_employed_for_all(*args, **kwargs):
    """Update days employed for all employees based on their hired_on date."""
    
    employees = frappe.get_all("Employee", ["name", "hired_on"])
    for emp in employees:
        if emp.workflow_state == "Hired" and emp.hired_on:
            days = (today() - getdate(emp.hired_on)).days
            frappe.db.set_value("Employee", emp.name, "days_employed", days, update_modified=False)
    frappe.db.commit()