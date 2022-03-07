import frappe

from non_profit.setup import setup_non_profit


def get_company():
	company = frappe.defaults.get_defaults().company
	if company:
		return company
	else:
		company = frappe.get_list("Company", limit=1)
		if company:
			return company[0].name
	return None


def before_tests():
	# complete setup if missing
	from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
	if not frappe.get_list("Company"):
		setup_complete({
			"currency"          :"USD",
			"full_name"         :"Test User",
			"company_name"      :"Frappe Care LLC",
			"timezone"          :"America/New_York",
			"company_abbr"      :"WP",
			"industry"          :"Healthcare",
			"country"           :"United States",
			"fy_start_date"     :"2021-01-01",
			"fy_end_date"       :"2021-12-31",
			"language"          :"english",
			"company_tagline"   :"Testing",
			"email"             :"test@erpnext.com",
			"password"          :"test",
			"chart_of_accounts" : "Standard",
			"domains"           : ["Non Profit"],
		})
		setup_non_profit()
