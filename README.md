# Employee Management App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./license.txt)
[![CI](https://github.com/MostafaKadry/frappe-employee-app/actions/workflows/ci.yml/badge.svg)](https://github.com/MostafaKadry/frappe-employee-app/actions/workflows/ci.yml)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)

A comprehensive Employee Management System built on the [Frappe Framework](https://frappeframework.com/), designed to streamline HR processes and employee data management with a modern, modular, and extensible architecture.

---

## 🚀 Features

### Employee Management
- **Comprehensive Profiles**: Track detailed employee information including contact details, position, and employment status
- **Status Workflow**: Monitor employees through various stages (Application Received, Interview Scheduled, Hired, etc.)
- **Employment Tracking**: Automatic calculation of employment duration based on hire date
- **Department Assignment**: Organize employees into departments for better management
- **Company Structure**: Support for multiple companies within the same system

### Department Management
- **Hierarchical Structure**: Create and manage organizational departments
- **Employee Assignment**: Easily assign and reassign employees to departments
- **Department Analytics**: Track department size and composition

### Company Management
- **Multi-company Support**: Manage multiple companies within a single installation
- **Company-specific Data**: Maintain separate employee records for each company

### Reporting & Analytics
- Employee directory with advanced filtering
- Department-wise employee listings
- Employment status reports


### Security & Access Control
- Role-based permissions
- Field-level security


---

## 🔗 Project Links

- **Production Instance:** [employee-app-opal.vercel.app](https://employee-app-opal.vercel.app/) for sorry server subscription ended.
- **Frontend Repo:** [employee-app (frontend)](https://github.com/MostafaKadry/employee-app.git)

---

## 📦 Installation

### Prerequisites
- Frappe Framework installed and running
- Python 3.6+
- Node.js 14+ and npm 6+
- MariaDB 10.3+ / PostgreSQL 9.5+
- Redis (for background jobs)

### Installation Steps

1. **Using Bench (Recommended)**
   ```bash
   # Navigate to your bench directory
   cd $PATH_TO_YOUR_BENCH
   
   # Get the app from GitHub
   bench get-app https://github.com/MostafaKadry/frappe-employee-app --branch develop
   
   # Install the app to your site
   bench --site yoursite.local install-app employee_app
   
   # Run database migrations
   bench --site yoursite.local migrate
   ```


2. **Post-Installation**
   - Clear cache: `bench clear-cache`
   - Restart the bench: `bench restart`
   - Set up background jobs: `bench setup supervisor`
3. **resoter backups**
- I recommened to use this data because workflow is stored in database.
   - `bench --site yoursite.local restore employee_app/backups/20250814_180003-employee_site-database.sql.gz`
   - `bench --site yoursite.local migrate`

For more details, refer to the [Frappe Installation Guide](https://frappeframework.com/docs/user/en/installation).

---

## 📚 Usage

### Getting Started

1. **Accessing the App**
   - Log in to your Frappe Desk
   - Navigate to the "Employee App" module

2. **Employee Management**
   - **Adding Employees**: Create new employee records with personal and professional details
   - **Employee Status**: Track employees through various stages (Application, Interview, Hired, etc.)
   - **Documents**: Attach important documents to employee records

3. **Department Management**
   - Create and manage departments
   - Assign employees to departments
   - View department-wise employee distribution

4. **Company Management**
   - Set up company profiles
   - Manage company-specific employee records
   - Configure company policies and settings

### Key Features

- **Employee Dashboard**: Quick overview of employee statistics
- **Advanced Search**: Find employees using various filters
- **Bulk Operations**: Import/Export employee data
- **Custom Fields**: Extend employee records as needed
- **Role-based Access**: Control who can view or edit sensitive information

### Mobile Responsive
Access and manage your employee data on-the-go with our mobile-responsive interface.
---

## 🖼️ Screenshots


**Employee App Databse ERD**
![Employee APP ERD](employee_app/public/images/empployee-app-erd.png)

**Client Side Dashboard**
![Dashboard](/employee_app/public/images/dashbord.png)


**Employee Wrokflow**
![WorkFlow](employee_app/public/images/employee_workflow.png)


**Employee Report using NextJs code**
![Department Overview](employee_app/public/images/employee_report.png)


---

## 🌐 Demo

Want to see it in action?  
👉 **[Try the Employee App Live](https://employee-app-opal.vercel.app/)**

---

## ❓ FAQ

>
> **Q: Is the frontend open-source?**  
> **A:** Yes! [employee-app frontend repo](https://github.com/MostafaKadry/employee-app.git)

---

## 🧑‍💻 Support

- **Issues & Bugs**: [GitHub Issues](https://github.com/MostafaKadry/frappe-employee-app/issues)
- **Discussions/Questions**: [GitHub Discussions](https://github.com/MostafaKadry/frappe-employee-app/discussions)
- **Email**: mostafakadry806@gmail.com

---

## 📅 Roadmap
- what done ?
- Build Backend Modules
- Create a API that supports all CRUD operations for all models
- Automatically calculate the number of departments and employees in the company
- Automatically calculate the number of employees in the department
- Automatically calculate the number of days an employee has been with the company based on the hiring date using Cron Job Hooks
- Handle cascading deletions
- Workflow, Developed a workflow to model the onboarding process for new employees
- Used Read Frappe User Module to Implement role-based access control.
- Ensure that authentication and authorization is always handled throughout user activity
- what not done yet?
- [ ] Add API documentation
- [ ] DB Queries Pagination
- [ ] integrate workflow actions with frontend
- [ ] Include unit tests
- [ ] Include integration tests

---



## 🙏 Acknowledgements

- Powered by [Frappe Framework](https://frappeframework.com/)

