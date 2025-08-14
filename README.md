# Employee App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./license.txt)
[![CI](https://github.com/MostafaKadry/frappe-employee-app/actions/workflows/ci.yml/badge.svg)](https://github.com/MostafaKadry/frappe-employee-app/actions/workflows/ci.yml)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)

A modern, modular, and extensible Employee Management App built on [Frappe Framework](https://frappeframework.com/). Manage employees, departments, and companies with robust reporting, permissions, and developer-friendly practices.

---

## 🚀 Features

- **Employee Management**: Create, update, and organize employee records.
- **Department & Company Modules**: Structure your organization for efficient management.
- **Reporting**: Built-in employee reports for insights and analytics.
- **Permissions & Security**: Fine-grained access control for sensitive data.
- **APIs**: Easily access department and employee data programmatically.
- **Extensible**: Designed to be customized and expanded for your needs.

---

## 🔗 Project Links

- **Production Instance:** [employee-app-opal.vercel.app](https://employee-app-opal.vercel.app/)
- **Frontend Repo:** [employee-app (frontend)](https://github.com/MostafaKadry/employee-app.git)

---

## 📦 Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/MostafaKadry/frappe-employee-app --branch develop
bench install-app employee_app
```

For more details, see [Frappe App Installation Guide](https://frappeframework.com/docs/user/en/installation).

---

## ⚡ CI/CD

- **CI**: GitHub Actions - installs and tests app on every push to `develop`.
- **Linters**: [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every PR.

---

## 📚 Usage

After installation, access modules via Frappe Desk:

- **Employee**: Add/edit/view employees.
- **Department**: Organize employees by department.
- **Company**: Manage company entities.
- **Reports**: Generate employee reports.

---

## 🖼️ Screenshots



**Employee Wrokflow**
![WorkFlow](employee_app/public/images/employee_workflow.png)


**Employee Wrokflow**
![Employee List](https://employee-app-opal.vercel.app/_next/image?url=%2Fimages%2Femployee-list.png&w=800&q=75)

**Department Overview**
![Department Overview](https://employee-app-opal.vercel.app/_next/image?url=%2Fimages%2Fdepartment-overview.png&w=800&q=75)

**Company Dashboard**
![Company Dashboard](https://employee-app-opal.vercel.app/_next/image?url=%2Fimages%2Fcompany-dashboard.png&w=800&q=75)


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
- what not done yet?
- [ ] Add RESTful API documentation
- [ ] DB Queries Pagination
- [ ] UI enhancements

---



## 🙏 Acknowledgements

- Powered by [Frappe Framework](https://frappeframework.com/)

