import frappe
from datetime import datetime,date
from math import floor
import datetime
from frappe.utils import add_days, cint, date_diff, format_date, getdate , today
from erpnext.accounts.utils import get_fiscal_year

def validate_loan_application(self,method):
    base_salary=0
    allowed_percent=0

    if self.applicant_type != "Employee":return

    if self.loan_amount:
        if frappe.db.exists("Salary Structure Assignment",{'Employee':self.applicant}):
            try:
                base_salary=frappe.db.sql("""select base from `tabSalary Structure Assignment` where Employee='{}' order by from_date DESC limit 1""".format(self.applicant),as_dict=1)[0]['base']
            except:
                base_salary=0
    
    if base_salary<=0:
        frappe.throw("Please add Salary Structure Assignment for Employee:{} to process Loan Application".format(self.applicant))
    
    date_of_joining=frappe.db.get_value("Employee",self.applicant,"date_of_joining")
    days_diff=int((date.today()-date_of_joining).days)
    
    if days_diff<=182:allowed_percent=25
    elif days_diff>182 and days_diff<=365:allowed_percent=50
    elif days_diff>365:allowed_percent=75

    if self.loan_amount > (base_salary*(allowed_percent/100)):
        frappe.throw("You are not alowed to apply for Loan greater then {} value ".format((base_salary*(allowed_percent/100))))
 
def get_work_experience_using_method(
    method, current_work_experience, minimum_year_for_gratuity, employee
):
    if method == "Round off Work Experience":
        current_work_experience = round(current_work_experience)
    elif method == 'Exact Years':
        current_work_experience = current_work_experience
    else:
        current_work_experience = floor(current_work_experience)

    if current_work_experience < minimum_year_for_gratuity:
        frappe.throw(
            _("Employee: {0} have to complete minimum {1} years for gratuity").format(
                bold(employee), minimum_year_for_gratuity
            )
        )
    return current_work_experience

def create_leave_allocation(self, leave_period, date_difference):
    is_carry_forward = frappe.db.get_value("Leave Type", self.leave_type, "is_carry_forward")
    allocation = frappe.get_doc(
        dict(
            doctype="Leave Allocation",
            employee=self.employee,
            employee_name=self.employee_name,
            leave_type=self.leave_type,
            from_date=add_days(self.work_end_date, 1),
            to_date=add_days(self.work_end_date, 91),
            carry_forward=cint(is_carry_forward),
            new_leaves_allocated=date_difference,
            total_leaves_allocated=date_difference,
            description=self.reason,
        )
    )
    allocation.insert(ignore_permissions=True)
    allocation.submit()
    return allocation


def before_naming(self, method):
    
	if not self.get('amended_from') and not self.get('name'):
		if not self.get('company_series'):
			self.company_series = None
		
		if self.get('series_value'):
			if self.series_value > 0:
				name = naming_series_name(self.naming_series, self.company_series)
				check = frappe.db.get_value('Series', name, 'current', order_by="name")
				if check == 0:
					pass
				elif not check:
					frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))

				frappe.db.sql("update `tabSeries` set current = {} where name = '{}'".format(cint(self.series_value) - 1, name))

def naming_series_name(name, company_series=None):
	if company_series:
		name = name.replace('company_series', str(company_series))
	name = name.replace('YYYY', str(datetime.date.today().year))
	name = name.replace('YY', str(datetime.date.today().year)[2:])
	name = name.replace('MM', '{0:0=2d}'.format(datetime.date.today().month))
	name = name.replace('DD', '{0:0=2d}'.format(datetime.date.today().day))
	name = name.replace('#', '')
	name = name.replace('.', '')
	return name

def auto_before_naming(self, method):
    
	if not self.get('amended_from') and not self.get('name'):
		if self.get('series_value'):
			if self.series_value > 0:
				name = auto_naming_series_name(self.naming_series)
				check = frappe.db.get_value('Series', name, 'current', order_by="name")
				if check == 0:
					pass
				elif not check:
					frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))

				frappe.db.sql("update `tabSeries` set current = {} where name = '{}'".format(cint(self.series_value) - 1, name))

def auto_naming_series_name(name):
	name = name.replace('YYYY', str(datetime.date.today().year))
	name = name.replace('YY', str(datetime.date.today().year)[2:])
	name = name.replace('MM', '{0:0=2d}'.format(datetime.date.today().month))
	name = name.replace('DD', '{0:0=2d}'.format(datetime.date.today().day))
	name = name.replace('#', '')
	name = name.replace('.', '')
	return name

@frappe.whitelist()
def make_auto_repeat(doctype, docname, frequency="Daily", start_date=None, end_date=None):
	if not start_date:
		start_date = getdate(today())
	doc = frappe.new_doc("Auto Repeat")
	doc.reference_doctype = doctype
	doc.reference_document = docname
	doc.series_value = frappe.db.get_value(doctype,docname,'auto_repeat_series_value')
	doc.frequency = frequency
	doc.start_date = start_date
	if end_date:
		doc.end_date = end_date
	doc.save()
	return doc

def send_notification(self, new_doc):
    recipient = []
    """Notify concerned people about recurring document generation"""
    subject = self.subject or ""
    message = self.message or ""

    if not self.subject:
        subject = _("New {0}: {1}").format(new_doc.doctype, new_doc.name)
    elif "{" in self.subject:
        subject = frappe.render_template(self.subject, {"doc": new_doc})

    print_format = self.print_format or "Standard"
    error_string = None

    try:
        attachments = [
            frappe.attach_print(
                new_doc.doctype, new_doc.name, file_name=new_doc.name, print_format=print_format
            )
        ]

    except frappe.PermissionError:
        error_string = _("A recurring {0} {1} has been created for you via Auto Repeat {2}.").format(
            new_doc.doctype, new_doc.name, self.name
        )
        error_string += "<br><br>"

        error_string += _(
            "{0}: Failed to attach new recurring document. To enable attaching document in the auto repeat notification email, enable {1} in Print Settings"
        ).format(frappe.bold(_("Note")), frappe.bold(_("Allow Print for Draft")))
        attachments = "[]"

    if error_string:
        message = error_string
    elif not self.message:
        message = _("Please find attached {0}: {1}").format(new_doc.doctype, new_doc.name)
    elif "{" in self.message:
        message = frappe.render_template(self.message, {"doc": new_doc})

    recipients = self.recipients.replace(",", "\n")
    recipient = recipient + recipients.split("\n")

    frappe.sendmail(
        reference_doctype=new_doc.doctype,
        reference_name=new_doc.name,
        recipients=recipient,
        subject=subject,
        message=message,
        attachments=attachments,
        print_letterhead=((attachments and attachments[0].get("print_letterhead")) or False)
    )