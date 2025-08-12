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

# READ - Get single employee
@frappe.whitelist(allow_guest=False)
def get_employee(**kwargs):
    """Get details for a single Employee."""
    name = kwargs.get("name")
    if not name:
        frappe.throw("Employee name is required.")
    if not frappe.has_permission(doctype="Employee", ptype="read", doc=name):
        frappe.throw("Not permitted", frappe.PermissionError)

    employee = frappe.db.get_value(
        "Employee", name, EMPLOYEE_READ_FIELDS, as_dict=True
    )
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


@frappe.whitelist(allow_guest=False)
def create_employee(*args, **kwargs):
    """Create a new Employee with all required fields."""

    if not frappe.has_permission("Employee", "create"):
        frappe.throw("Not permitted", frappe.PermissionError)
    kwargs.pop("cmd", None)
    
    # Validate all required fields
    missing_fields = [field for field in EMPLOYEE_WRITE_FIELDS if not kwargs.get(field)]
    if missing_fields:
        frappe.throw(f"Missing required fields: {', '.join(missing_fields)}")
    
    not_allowed_fields = set(kwargs.keys()) - set(EMPLOYEE_WRITE_FIELDS)
    
    if not_allowed_fields:
        frappe.throw(f"Not Allowed to add this fields: {', '.join(not_allowed_fields)}")

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
            "Employee",
            doc.name,
            EMPLOYEE_READ_FIELDS,
            as_dict=True
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

    employee.save()
    frappe.db.commit()

    # Return updated employee with read-safe fields
    return frappe.db.get_value(
        "Employee",
        employee.name,
        EMPLOYEE_READ_FIELDS,
        as_dict=True
    )


# DELETE - Remove an employee
@frappe.whitelist(allow_guest=False)    
def delete_employee(**kwargs):
    """Delete an Employee."""
    if not frappe.has_permission(doctype="Employee", ptype="delete", doc=kwargs["name"]):
        frappe.throw("Not permitted", frappe.PermissionError)

    frappe.delete_doc("Employee", kwargs["name"])
    frappe.db.commit()

    return {"message": f"Employee '{kwargs["name"]}' deleted successfully."}