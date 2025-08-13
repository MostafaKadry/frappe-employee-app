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
- **Modern Dev Practices**: Pre-commit hooks, CI/CD, linting, and code formatting.

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

## 🛠️ Contributing

We use [pre-commit](https://pre-commit.com/) for code formatting and linting.
To get started:

```bash
cd apps/employee_app
pre-commit install
```

Pre-commit hooks for:
- [ruff](https://github.com/astral-sh/ruff) (Python)
- [eslint](https://eslint.org/) (JS)
- [prettier](https://prettier.io/) (JS/JSON/Markdown)
- [pyupgrade](https://github.com/asottile/pyupgrade) (Python)

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

API examples:

```python
# List departments
frappe.call("employee_app.api.department.list_departments")

# Get employees by department
frappe.call("employee_app.api.department.get_department_related_employees", name="IT")
```

---

## 🖼️ Screenshots

> _Add screenshots of the UI, reports, or dashboards here!_
>
> ![Screenshot Placeholder](https://via.placeholder.com/600x300?text=Screenshot)

---

## 🌐 Demo

> _Add link to your live demo or hosted instance here!_
>
> [Try the Employee App Live](#)

---

## ❓ FAQ

> _Add frequently asked questions here!_
>
> **Q: What is the minimum Frappe version required?**  
> **A:** v14+

> **Q: How do I add custom fields to Employee?**  
> **A:** Use Frappe's DocType customization features.

---

## 🧑‍💻 Support

- **Issues & Bugs**: [GitHub Issues](https://github.com/MostafaKadry/frappe-employee-app/issues)
- **Discussions/Questions**: [GitHub Discussions](https://github.com/MostafaKadry/frappe-employee-app/discussions)
- **Email**: mostafakadry806@gmail.com

---

## 📅 Roadmap

- [ ] Add more advanced reporting features
- [ ] Integrate leave and attendance modules
- [ ] Add RESTful API documentation
- [ ] UI enhancements

---

## 📜 License

MIT - see [license.txt](./license.txt) for details.

---

## 🙏 Acknowledgements

- Powered by [Frappe Framework](https://frappeframework.com/)
- Inspired by open-source HR solutions

---

> _Feel free to customize this README with your branding, screenshots, demos, and more!_
