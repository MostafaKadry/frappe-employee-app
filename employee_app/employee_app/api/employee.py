import frappe

EMPLOYEE_READ_FIELDS = [
    "name",
    "employee_name",
    "status",
    "email_address",
    "mobile_number",
    "department",
    "company",
    "address",
    "designation_positiontitle",
    "hired_on",
    "days_employed",
]
EMPLOYEE_WRITE_FIELDS = [
    "employee_name",
    "email_address",
    "mobile_number",
    "department",
    "company",
    "address",
    "designation_positiontitle",
]
restricted_fields = {
    "status": "Status cannot be set manually. It is automatically updated based on employment status.",
    "hired_on": "Hired On date cannot be set manually. It is automatically set to the current date when the employee is hired.",
    "days_employed": "Days Employed cannot be set manually. It is automatically calculated based on the Hired On date.",
}


def is_restricted_field(field):
    """Check if a field is restricted from manual setting."""
    return field in restricted_fields


# API Response Helper Fn
def api_response(status_code, message, data=None):
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = message
    frappe.local.response["data"] = data
    return frappe.local.response


# READ - Get single employee
@frappe.whitelist(allow_guest=False)
def get_employee(**kwargs):
    """Get details for a single Employee."""
    name = kwargs.get("name")
    if not name:
        frappe.throw("Employee name is required.")
    if not frappe.has_permission(doctype="Employee", ptype="read", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    employee = frappe.db.get_value("Employee", name, EMPLOYEE_READ_FIELDS, as_dict=True)
    if not employee:
        frappe.throw(f"Employee '{name}' not found.")
    return employee


# READ - List employees
@frappe.whitelist(allow_guest=False)
def list_employees():
    """List all employees the user can access."""
    if not frappe.has_permission("Employee", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    employees = frappe.get_all("Employee", fields=EMPLOYEE_READ_FIELDS)
    return employees


# READ - Get employees count
@frappe.whitelist(allow_guest=False)
def get_all_employees_count():
    """Get the total number of employees."""
    if not frappe.has_permission("Employee", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)

    employee_count = frappe.db.count("Employee")
    api_response(
        status_code=200,
        message="Total number of employees retrieved successfully.",
        data={"total_employees": employee_count},
    )
    # return {"total_employees": employee_count} --- IGNORE ---


# read - get recently hired employees
@frappe.whitelist(allow_guest=False)
def get_recently_hired_employees():
    """Get employees hired within the last 'days' days."""
    if not frappe.has_permission("Employee", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    # to be done  get the real hired employees for now it just retrun last 5 add employees
    employees = frappe.get_all(
        "Employee", order_by="creation desc", limit=5, fields=EMPLOYEE_READ_FIELDS
    )

    if not employees:
        api_response(
            status_code=404, message="No recently hired employees found.", data=[]
        )

    api_response(
        status_code=200,
        message="Employees hired in the last few days retrieved successfully.",
        data=employees,
    )


# CREATE - Add a new employee
@frappe.whitelist(allow_guest=False)
def create_employee(*args, **kwargs):
    """Create a new Employee with all required fields."""

    if not frappe.has_permission("Employee", "create"):
        frappe.throw("Not permitted", frappe.PermissionError)

    # Validate all required fields
    missing_fields = [field for field in EMPLOYEE_WRITE_FIELDS if not kwargs.get(field)]
    if missing_fields:
        frappe.throw(f"Missing required fields: {', '.join(missing_fields)}")

    for field in kwargs:
        if is_restricted_field(field):
            frappe.throw(
                f"{field} cannot be set manually. It is updated automatically."
            )

    employee_data = {"doctype": "Employee"}
    for field in EMPLOYEE_WRITE_FIELDS:
        employee_data[field] = kwargs[field]

    # Insert the new Employee
    doc = frappe.get_doc(employee_data)
    doc.insert()
    frappe.db.commit()

    # Return the created Employee (read-safe fields only)
    return {
        "message": frappe.db.get_value(
            "Employee", doc.name, EMPLOYEE_READ_FIELDS, as_dict=True
        )
    }


# UPDATE - Update an existing employee
@frappe.whitelist(allow_guest=False)
def update_employee(name, **kwargs):
    """Update an existing Employee."""
    if not name:
        frappe.throw("Employee name is required.")
    employee = frappe.get_doc("Employee", name)

    if not employee.has_permission("write"):
        frappe.throw("Not permitted", frappe.PermissionError)

    # Ensure all required fields are present in kwargs
    missing_fields = [f for f in EMPLOYEE_WRITE_FIELDS if f not in kwargs]
    if missing_fields:
        frappe.throw(f"Missing required fields: {', '.join(missing_fields)}")

    for field in EMPLOYEE_WRITE_FIELDS:
        employee.set(field, kwargs[field])
    # Prevent manual setting of restricted fields
    for field in kwargs:
        if is_restricted_field(field):
            frappe.throw(
                f"{field} cannot be set manually. It is updated automatically."
            )

    employee.save()
    frappe.db.commit()

    # Return updated employee with read-safe fields
    return frappe.db.get_value(
        "Employee", employee.name, EMPLOYEE_READ_FIELDS, as_dict=True
    )


# DELETE - Remove an employee
@frappe.whitelist(allow_guest=False)
def delete_employee(**kwargs):
    """Delete an Employee."""
    if not frappe.has_permission(
        doctype="Employee", ptype="delete", doc=kwargs["name"]
    ):
        frappe.throw("Not permitted", frappe.PermissionError)

    frappe.delete_doc("Employee", kwargs["name"])
    frappe.db.commit()

    return {"message": f"Employee '{kwargs["name"]}' deleted successfully."}
