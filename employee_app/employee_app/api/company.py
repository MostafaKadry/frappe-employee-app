import frappe
from .department import DEPARTMENT_READ_FIELDS
from .employee import EMPLOYEE_READ_FIELDS

COMPANY_READ_FIELDS = [
    "name",
    "company_name",
    "number_of_departments",
    "number_of_employees",
]

COMPANY_WRITE_FIELDS = ["company_name"]
# utility functions
# function to check if send restricted fields
def is_restricted_field(field):
    """Check if the field is restricted from manual editing."""
    restricted_fields = ["number_of_employees", "number_of_departments"]
    return field in restricted_fields

# API Response Helper Fn
def api_response(status_code, message, data=None):
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = message
    frappe.local.response["data"] = data
    return frappe.local.response

# READ - Get single company
@frappe.whitelist(allow_guest=False)
def get_company(*args, **kwargs):
    """Get details for a single Company."""
    name = kwargs.get("name")
    if not name:
        api_response(
            status_code=400,
            message="Company name is required.",
            data=None
        )
        return

    # Fetch company details
    company = frappe.db.get_value(
        "Company", name, COMPANY_READ_FIELDS, as_dict=True
    )
    if not company:
        api_response(
            status_code=404,
            message=f"Company '{name}' not found.",
            data=None
        )
        return
    # get related departments and employees
    departments = get_company_related_departments(company=name)
    employees = get_company_related_employee(company=name)
    
    api_response(
        status_code=200,
        message=f"Company '{name}' retrieved successfully.",
        data={
            "company": company,
            "departments": departments,
            "employees": employees
        }
    )

# READ - List companies
@frappe.whitelist(allow_guest=False)
def list_companies():
    """List all companies the user can access."""
    companies = frappe.get_all("Company", fields=COMPANY_READ_FIELDS)
    return companies

# READ - Get departments related to a specific company
@frappe.whitelist(allow_guest=False)
def get_company_related_departments(*args, **kwargs):
    """Get all departments related to a specific company."""
    company = kwargs.get("company")
    if not company:
        frappe.throw("Company name is required.")

    departments = frappe.get_all(
        "Department",
        filters={"company": company},
        fields=DEPARTMENT_READ_FIELDS
    )
    
    return departments

# READ -Get Employyes related to company 
@frappe.whitelist(allow_guest=False)
def get_company_related_employee(*args, **kwargs):
    """Get all employees related to a specific company."""
    company = kwargs.get("company")
    if not company:
        frappe.throw("Company name is required.")

    employees = frappe.get_all(
        "Employee",
        filters={"company": company},
        fields=EMPLOYEE_READ_FIELDS
    )
    
    return employees

# READ - Get all companies count
@frappe.whitelist(allow_guest=False)
def get_all_companies_count():
    """Get the total number of companies."""   
    company_count = frappe.db.count("Company")
    api_response(
        status_code=200,
        message="Total number of companies retrieved successfully.",
        data={"total_companies": company_count}
    )

# CREATE - Add a new company
@frappe.whitelist(allow_guest=False)
def create_company(**kwargs):
    """Create a new Company."""
    company_name = kwargs.get("company_name")

    if not company_name:
        frappe.throw("Company name is required.")
    for field in kwargs:
        if is_restricted_field(field):
            frappe.throw(f"{field} cannot be set manually. It is updated automatically.")

    # Create and insert the new company document
    doc = frappe.get_doc({"doctype": "Company", "company_name": company_name})
    doc.insert()
    frappe.db.commit()

    return frappe.db.get_value("Company", doc.name, COMPANY_READ_FIELDS, as_dict=True)


# UPDATE
@frappe.whitelist(allow_guest=False)
def update_company(**kwargs):
    """Update the company_name"""
    
    name = kwargs.get("name")
    company_name = kwargs.get("company_name")

    if not name:
        frappe.throw("Company 'name' is required.")
    if not company_name:
        frappe.throw("'company_name' is required for update.")
    for field in kwargs:
        if is_restricted_field(field):
            frappe.throw(f"{field} cannot be set manually. It is updated automatically.")
    company = frappe.get_doc("Company", name)

    if not company.has_permission("write"):
        frappe.throw("Not permitted", frappe.PermissionError)

    company.company_name = company_name
    company.save()
    frappe.db.commit()

    return frappe.db.get_value(
            "Company",
            company.name,
            COMPANY_READ_FIELDS,
            as_dict=True
        )
  

# DELETE - Remove a company
@frappe.whitelist(allow_guest=False)
def delete_company(**kwargs):
    name = kwargs.get("name")
    if not name:
        frappe.response["message"] = "Company name is required."
        frappe.response["http_status_code"] = 400
        return
    """Delete a Company."""
    company = frappe.get_doc("Company", name)
    if not company:
        frappe.throw(f"Company '{name}' not found.")
        
    """" Check if the company has related departments or employees before deletion and delete related departments and employees if they exist. CASECADING DELETE """
    related_departments = frappe.db.get_all("Department", {"company": name})
    if related_departments:
        for department in related_departments:
            frappe.delete_doc("Department", department.name)
    
    related_employees = frappe.db.get_all("Employee", {"company": name})
    if related_employees:
        for employee in related_employees:
            frappe.delete_doc("Employee", employee.name)

    # Finally, delete the company document
    frappe.delete_doc("Company", name)
    frappe.db.commit()
    return {"message": f"Company '{name}' deleted successfully."}
