# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def setup(company=None, patch=True):
	make_custom_fields()


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
			dict(fieldname='non_profit_column_break', fieldtype='Column Break', insert_after='with_effect_from'),
			dict(fieldname='pan_details', label='PAN Number',
				fieldtype='Data', insert_after='with_effect_from')
		]
	}
	return custom_fields

