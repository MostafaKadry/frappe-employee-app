import frappe
from .employee import EMPLOYEE_READ_FIELDS

DEPARTMENT_READ_FIELDS = [
    "name",
    "department_name",
    "company",
    "number_of_employees",
]

DEPARTMENT_WRITE_FIELDS = ["department_name", "company"]
RESTRICTED_FIELDS = ["number_of_employees"]
# API Response Helper Fn
def api_response(status_code, message, data=None):
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = message
    frappe.local.response["data"] = data
    return frappe.local.response


# READ - Get single department
@frappe.whitelist(allow_guest=False)
def get_department(**kwargs):
    """Get details for a single Department."""
    if not frappe.has_permission(
        doctype="Department", ptype="read", doc=kwargs["name"]
    ):
        frappe.throw("Not permitted", frappe.PermissionError)

    department = frappe.db.get_value(
        "Department", kwargs["name"], DEPARTMENT_READ_FIELDS, as_dict=True
    )
    if not department:
        frappe.throw(f"Department '{kwargs['name']}' not found.")
    return department


# READ - List departments
@frappe.whitelist(allow_guest=False)
def list_departments():
    """List all departments the user can access."""
    if not frappe.has_permission("Department", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    departments = frappe.get_all("Department", fields=DEPARTMENT_READ_FIELDS)
    return departments


# READ - Get employees related to a specific department
@frappe.whitelist(allow_guest=False)
def get_department_related_employees(*args, **kwargs):
    """Get all employees related to a specific department."""
    department = kwargs.get("name")
    if not department:
        frappe.throw("Department name is required.")

    if not frappe.has_permission(doctype="Employee", ptype="read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    department_company = frappe.db.get_value("Department", department, "company")
    employees = frappe.get_all(
        "Employee",
        filters={"department": department, "company": department_company},
        fields=EMPLOYEE_READ_FIELDS,
    )

    return employees


# CREATE - Add a new department
@frappe.whitelist(allow_guest=False)
def create_department(**kwargs):
    """Create a new Department linked to a company."""
    department_name = kwargs.get("department_name")
    company = kwargs.get("company")

    # Check create permission
    if not frappe.has_permission("Department", "create"):
        frappe.throw("Not permitted", frappe.PermissionError)

    # Required fields check
    if not department_name or not company:
        frappe.throw("Department name and company are required.")

    # Prevent manual setting of restricted fields
    restricted_sent = [field for field in RESTRICTED_FIELDS if kwargs.get(field) is not None]
    if restricted_sent:
        frappe.throw(f"Fields {', '.join(restricted_sent)} cannot be set manually.")

    # Create document
    doc = frappe.new_doc("Department")
    doc.department_name = department_name
    doc.company = company
    doc.insert(ignore_permissions=False)  # obey permissions

    # Fetch created record
    department = frappe.db.get_value(
        "Department", doc.name, DEPARTMENT_READ_FIELDS, as_dict=True
    )

    # Send API response
    api_response(
        status_code=201,
        message="Department created successfully.",
        data=department,
    )

# UPDATE - Update an existing department
@frappe.whitelist(allow_guest=False)
def update_department(**kwargs):
    name = kwargs.get("name")
    department_name = kwargs.get("department_name")
    company = kwargs.get("company")
    """Update the department_name and company of an existing Department."""
    if not frappe.has_permission(doctype="Department", ptype="write", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    if not name or not department_name or not company:
        frappe.throw("New department name and company are required.")
    
    restricted_sent = [field for field in RESTRICTED_FIELDS if kwargs.get(field) is not None]
    if restricted_sent:
        frappe.throw(f"Fields {', '.join(restricted_sent)} cannot be set manually.")

    doc = frappe.get_doc("Department", name)
    doc.department_name = department_name
    doc.company = company
    doc.save()
    frappe.db.commit()

    api_response(
        status_code=200,
        message="Department updated successfully.",
        data=frappe.db.get_value(
            "Department", name, DEPARTMENT_READ_FIELDS, as_dict=True
        ),
    )


# DELETE - Remove a department
@frappe.whitelist(allow_guest=False)
def delete_department(**kwargs):
    """Delete a Department."""

    name = kwargs["name"]
    if not name:
        frappe.throw("Department Name is required (ID)")

    if not frappe.has_permission(doctype="Department", ptype="delete", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    if not frappe.db.exists("Department", name):
        frappe.throw(f"Department '{name}' does not exist.")

    frappe.delete_doc("Department", name)
    frappe.db.commit()

    return {"message": f"Department '{name}' deleted successfully."}

# GET - Get total count of all departments
@frappe.whitelist(allow_guest=False)
def get_all_depratments_count(*args, **kwargs):
    """Get the total count of all departments."""
    if not frappe.has_permission("Department", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)

    department_count = frappe.db.count("Department")
    api_response(
        status_code=200,
        message="Total department count retrieved successfully.",
        data={"total_departments": department_count},
    )
    