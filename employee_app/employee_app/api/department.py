import frappe

DEPARTMENT_READ_FIELDS = [
    "name",
    "department_name",
    "company",
    "number_of_employees",
]

DEPARTMENT_WRITE_FIELDS = ["department_name", "company"]


# READ - Get single department
@frappe.whitelist(allow_guest=False)
def get_department(department_name):
    """Get details for a single Department."""
    if not frappe.has_permission(doctype="Department", ptype="read", doc=department_name):
        frappe.throw("Not permitted", frappe.PermissionError)

    department = frappe.db.get_value(
        "Department", department_name, DEPARTMENT_READ_FIELDS, as_dict=True
    )
    if not department:
        frappe.throw(f"Department '{department_name}' not found.")
    return department

# READ - List departments
@frappe.whitelist(allow_guest=False)
def list_departments():
    """List all departments the user can access."""
    if not frappe.has_permission("Department", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    departments = frappe.get_all("Department", fields=DEPARTMENT_READ_FIELDS)
    return departments

# CREATE - Add a new department
@frappe.whitelist(allow_guest=False)
def create_department(department_name, company):
    if not frappe.has_permission("Department", "create"):
        frappe.throw("Not permitted", frappe.PermissionError)
    if not department_name or not company:
        frappe.throw("Department name and company are required.")

    doc = frappe.get_doc({
        "doctype": "Department",
        "department_name": department_name,
        "company": company
    })
    doc.insert()
    frappe.db.commit()

    return frappe.db.get_value("Department", doc.name, DEPARTMENT_READ_FIELDS, as_dict=True)

# UPDATE - Update an existing department
@frappe.whitelist(allow_guest=False)
def update_department(department_name, new_department_name, new_company):
    """Update the department_name and company of an existing Department."""
    if not frappe.has_permission(doctype="Department", ptype="write", doc=department_name):
        frappe.throw("Not permitted", frappe.PermissionError)

    if not new_department_name or not new_company:
        frappe.throw("New department name and company are required.")

    doc = frappe.get_doc("Department", department_name)
    doc.department_name = new_department_name
    doc.company = new_company
    doc.save()
    frappe.db.commit()

    return frappe.db.get_value("Department", doc.name, DEPARTMENT_READ_FIELDS, as_dict=True)

# DELETE - Remove a department
@frappe.whitelist(allow_guest=False)
def delete_department(department_name):
    """Delete a Department."""
    if not frappe.has_permission(doctype="Department", ptype="delete", doc=department_name):
        frappe.throw("Not permitted", frappe.PermissionError)

    if not frappe.db.exists("Department", department_name):
        frappe.throw(f"Department '{department_name}' does not exist.")

    frappe.delete_doc("Department", department_name)
    frappe.db.commit()

    return {"message" : f"Department '{department_name}' deleted successfully."}