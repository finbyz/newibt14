import frappe
from frappe.utils import flt
from frappe.utils import date_diff
from datetime import datetime
from dateutil import relativedelta

def validate(self, method):
	if self.date_of_joining and self.relieving_date:
		diff_days = date_diff(self.relieving_date,self.date_of_joining )
		self.total_days=diff_days or 0

		start_date = datetime.strptime(str(self.date_of_joining), "%Y-%m-%d")
		end_date =  datetime.strptime(str(self.relieving_date), "%Y-%m-%d")

		delta = relativedelta.relativedelta(end_date, start_date)
		duration = str(str(delta.years)+ 'Years,'+str( delta.months)+ ' months')
		
		self.duration=duration or 0



@frappe.whitelist()
def get_salary_structure_assignment(employee):
	data = frappe.db.sql(f""" SELECT name  From `tabSalary Structure Assignment`  where employee = '{employee}' Order By from_date DESC Limit 1""",as_dict = 1)
	if not data:
		return None
	return data[0].name