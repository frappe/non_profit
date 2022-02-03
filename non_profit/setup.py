import frappe
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def make_custom_records():
	records = [
		{'doctype': "Party Type", "party_type": "Member", "account_type": "Receivable"},
		{'doctype': "Party Type", "party_type": "Donor", "account_type": "Receivable"},
	]
	make_records(records)


def setup_non_profit():
	make_custom_records()
	make_custom_fields()

	has_domain = frappe.get_doc({
		'doctype': 'Has Domain',
		'parent': 'Domain Settings',
		'parentfield': 'active_domains',
		'parenttype': 'Domain Settings',
		'domain': 'Non Profit',
	})
	has_domain.save()

	domain = frappe.get_doc('Domain', 'Non Profit')
	domain.setup_domain()

	domain_settings = frappe.get_single('Domain Settings')
	domain_settings.append('active_domains', dict(domain=domain))
	frappe.clear_cache()


data = {
	'on_setup': 'non_profit.setup.setup_non_profit'
}


def make_custom_fields(update=True):
	custom_fields = get_custom_fields()
	create_custom_fields(custom_fields, update=update)


def get_custom_fields():
	custom_fields = {
		'Company': [
			dict(fieldname='non_profit_section', label='Non Profit Settings',
				 fieldtype='Section Break', insert_after='asset_received_but_not_billed', collapsible=1),
			dict(fieldname='company_80g_number', label='80G Number',
				 fieldtype='Data', insert_after='non_profit_section'),
			dict(fieldname='with_effect_from', label='80G With Effect From',
				 fieldtype='Date', insert_after='company_80g_number'),
			dict(fieldname='non_profit_column_break', fieldtype='Column Break',
				 insert_after='with_effect_from'),
			dict(fieldname='pan_details', label='PAN Number',
				 fieldtype='Data', insert_after='with_effect_from')
		],
		'Member': [
			{
				'fieldname': 'pan_number',
				'label': 'PAN Details',
				'fieldtype': 'Data',
				'insert_after': 'email_id'
			}
		],
		'Donor': [
			{
				'fieldname': 'pan_number',
				'label': 'PAN Details',
				'fieldtype': 'Data',
				'insert_after': 'email'
			}
		],
	}
	return custom_fields
