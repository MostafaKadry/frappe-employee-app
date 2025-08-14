import frappe

# Local imports
from .company import list_companies
from .employee import get_recently_hired_employees, get_all_employees_count
from .department import get_all_depratments_count  

def api_response(status_code, message, data=None):
    """
    Standardized API response helper.
    """
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = message
    frappe.local.response["data"] = data
    return frappe.local.response


@frappe.whitelist(allow_guest=False)
def get_dashboard_stats(*args, **kwargs):
    """
    Fetch dashboard statistics including companies, recent hires,
    employee count, and department count.
    """
    try:
        companies = list_companies()
        recent_employees = get_recently_hired_employees()
        employees_count = get_all_employees_count()
        department_count = get_all_depratments_count()

        api_response(
            status_code=200,
            message="Dashboard data returned successfully",
            data={
                "companies": companies,
                "recent_employees": recent_employees,
                "employees_count": employees_count,
                "department_count": department_count
            }
        )
    except Exception as e:
        frappe.log_error(f"Dashboard API Error: {str(e)}", "get_dashboard_stats")
        api_response(
            status_code=500,
            message="Failed to retrieve dashboard data",
            data=None
        )
