# Copyright (c) 2022, ibt and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OvertimeSalary(Document):
	def validate(self):
		self.ot_calculation()
	
	def on_submit(self):
		self.create_salary_structure_assignment()

	def ot_calculation(self):
		base = frappe.db.get_value("Salary Structure Assignment",self.salary_structure_assignment,'base')
		week_amount = ((((base/2) * 12) / (365 * 8 ) )* self.hours)
		if self.based_on == 'OT On Weekday':
			self.amount =  week_amount * 1.25
		if self.based_on == 'OT On Weekend' or self.based_on == 'Working On Public Holiday':
			self.amount = week_amount * 1.5
		
	
	def create_salary_structure_assignment(self):
		doc = frappe.new_doc('Additional Salary')
		doc.payroll_date = self.payroll_date
		doc.employee = self.employee
		doc.amount = self.amount
		doc.salary_component = 'Over Time'
		doc.save()
		doc.submit()



@frappe.whitelist()
def get_salary_structure_assignment(employee):
	data = frappe.db.sql(f""" SELECT name  From `tabSalary Structure Assignment`  where employee = '{employee}' Order By from_date DESC Limit 1""",as_dict = 1)
	return data[0].name    