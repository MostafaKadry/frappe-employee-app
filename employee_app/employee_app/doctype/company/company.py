# Copyright (c) 2025, Mostafa K. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Company(Document):
	def validate(self):
		"""Prevent manual editing of number_of_employees."""
		restricted_fields = {
			"number_of_employees": "Number of employees should not be set manually.",
			"number_of_departments": "Number of departments should not be set manually."
		}

		for field, message in restricted_fields.items():
			if self.has_value_changed(field):
				frappe.throw(message)

	
