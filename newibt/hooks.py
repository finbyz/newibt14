from . import __version__ as app_version

app_name = "newibt"
app_title = "New Ibt"
app_publisher = "ibt"
app_description = "custom app"
app_email = "info@finbyz.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/newibt/css/newibt.css"
# app_include_js = "/assets/newibt/js/newibt.js"

# include js, css files in header of web template
# web_include_css = "/assets/newibt/css/newibt.css"
# web_include_js = "/assets/newibt/js/newibt.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "newibt/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "newibt.utils.jinja_methods",
#	"filters": "newibt.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "newibt.install.before_install"
# after_install = "newibt.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "newibt.uninstall.before_uninstall"
# after_uninstall = "newibt.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "newibt.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Shift Type": "newibt.new_ibt.shift_type.ShiftType",
	"Employee Checkin": "newibt.new_ibt.employee_checkin.EmployeeCheckin"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
doctype_js = {"Full and Final Statement" : "public/js/full_and_final_statement.js"}

doc_events = {
	"Loan Application": {
		"validate": "newibt.api.validate_loan_application"
	},
	"Full and Final Statement": {
		"validate": "newibt.new_ibt.doc_events.full_and_final_statement.validate"
	},
	("Sales Invoice","Sales Order"):{
		"before_naming":"newibt.api.before_naming",
	},
	"Auto Repeat":{
		"before_naming":"newibt.api.auto_before_naming",
	},
	"Employee Checkin":{
		"validate":"newibt.api.validate"
	}
	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"newibt.tasks.all"
#	],
#	"daily": [
#		"newibt.tasks.daily"
#	],
#	"hourly": [
#		"newibt.tasks.hourly"
#	],
#	"weekly": [
#		"newibt.tasks.weekly"
#	],
#	"monthly": [
#		"newibt.tasks.monthly"
#	],
# }
# scheduler_events = {
	
# 	"daily": [
# 		"newibt.api.update_last_sync_date_time"
# 	]
	
# }

# Testing
# -------

# before_tests = "newibt.install.before_tests"

# Overriding Methods
# ------------------------------
#

override_whitelisted_methods = {
	"frappe.automation.doctype.auto_repeat.auto_repeat.make_auto_repeat": "newibt.api.make_auto_repeat"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "newibt.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"newibt.auth.validate"
# ]

from hrms.hr.doctype.compensatory_leave_request.compensatory_leave_request import CompensatoryLeaveRequest
from newibt.api import create_leave_allocation
CompensatoryLeaveRequest.create_leave_allocation = create_leave_allocation

from hrms.hr.doctype.employee_checkin import employee_checkin
from newibt.new_ibt.employee_checkin import mark_attendance_and_link_log
employee_checkin.mark_attendance_and_link_log = mark_attendance_and_link_log

from hrms.payroll.doctype.gratuity import gratuity
from newibt.api import get_total_applicable_component_amount , calculate_employee_total_workings_days
gratuity.get_total_applicable_component_amount = get_total_applicable_component_amount
gratuity.calculate_employee_total_workings_days = calculate_employee_total_workings_days

from hrms.payroll.doctype.gratuity import gratuity
from newibt.api import get_work_experience_using_method
gratuity.get_work_experience_using_method = get_work_experience_using_method

# from frappe.automation.doctype.auto_repeat.auto_repeat import AutoRepeat
# from newibt.api import send_notification
# AutoRepeat.send_notification = send_notification