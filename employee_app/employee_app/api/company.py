import frappe


COMPANY_READ_FIELDS = [
    "name",
    "company_name",
    "number_of_departments",
    "number_of_employees",
]

COMPANY_WRITE_FIELDS = ["company_name"]


# READ - Get single company
@frappe.whitelist(allow_guest=False)
def get_company(name):
    """Get details for a single Company."""
    if not frappe.has_permission(doctype="Company", ptype="read", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    company = frappe.db.get_value(
        "Company", name, COMPANY_READ_FIELDS, as_dict=True
    )
    if not company:
        frappe.throw(f"Company '{name}' not found.")
    return company

# READ - List companies
@frappe.whitelist(allow_guest=False)
def list_companies():
    """List all companies the user can access."""
    if not frappe.has_permission("Company", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    companies = frappe.get_all("Company", fields=COMPANY_READ_FIELDS)
    return companies


# CREATE - Add a new company
@frappe.whitelist(allow_guest=False)
def create_company(company_name):
    if not frappe.has_permission("Company", "create"):
        frappe.throw("Not permitted", frappe.PermissionError)
    if not company_name:
        frappe.throw("Company name is required.")

    doc = frappe.get_doc({"doctype": "Company", "company_name": company_name})
    doc.insert()
    frappe.db.commit()

    return frappe.db.get_value("Company", doc.name, COMPANY_READ_FIELDS, as_dict=True)


# UPDATE
@frappe.whitelist(allow_guest=False)
def update_company(name, **krgs):
    """Update the company_name of an existing Company."""
    if not frappe.has_permission(doctype="Company", ptype="write", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    company = frappe.get_doc("Company", name)
    company.company_name = krgs.get("company_name", company.company_name)
    company.save()
    frappe.db.commit()

    return frappe.db.get_value(
        "Company", company.name, COMPANY_READ_FIELDS, as_dict=True
    )


# DELETE - Remove a company
@frappe.whitelist(allow_guest=False)
def delete_company(company_name):
    """Delete a Company."""
    if not frappe.has_permission(doctype="Company", ptype="delete", doc=company_name):
        frappe.throw("Not permitted", frappe.PermissionError)

    frappe.delete_doc("Company", company_name)
    frappe.db.commit()
    return {"message": f"Company '{company_name}' deleted successfully."}
