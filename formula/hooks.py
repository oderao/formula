app_name = "formula"
app_title = "Formula"
app_publisher = "Nigmacorp"
app_description = "ERPNext Customizations for formula.co.za"
app_email = "tripleo4u@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/formula/css/formula.css"
# app_include_js = "/assets/formula/js/formula.js"

# include js, css files in header of web template
# web_include_css = "/assets/formula/css/formula.css"
# web_include_js = "/assets/formula/js/formula.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "formula/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js",
              "Item" : "public/js/item.js"
              }

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "formula.utils.jinja_methods",
# 	"filters": "formula.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "formula.install.before_install"
# after_install = "formula.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "formula.uninstall.before_uninstall"
# after_uninstall = "formula.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "formula.utils.before_app_install"
# after_app_install = "formula.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "formula.utils.before_app_uninstall"
# after_app_uninstall = "formula.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "formula.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Item": "formula.overrides.CustomItem"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"formula.tasks.all"
# 	],
# 	"daily": [
# 		"formula.tasks.daily"
# 	],
# 	"hourly": [
# 		"formula.tasks.hourly"
# 	],
# 	"weekly": [
# 		"formula.tasks.weekly"
# 	],
# 	"monthly": [
# 		"formula.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "formula.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "formula.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "formula.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["formula.utils.before_request"]
# after_request = ["formula.utils.after_request"]

# Job Events
# ----------
# before_job = ["formula.utils.before_job"]
# after_job = ["formula.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"formula.auth.validate"
# ]
