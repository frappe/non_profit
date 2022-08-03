# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document

from payments.utils import get_payment_gateway_controller

class NonProfitSettings(Document):
	@frappe.whitelist()
	def generate_webhook_secret(self, field="membership_webhook_secret"):
		key = frappe.generate_hash(length=20)
		self.set(field, key)
		self.save()

		secret_for = "Membership" if field == "membership_webhook_secret" else "Donation"

		frappe.msgprint(
			_("Here is your webhook secret for {0} API, this will be shown to you only once.").format(secret_for) + "<br><br>" + key,
			_("Webhook Secret")
		)

	@frappe.whitelist()
	def revoke_key(self, key):
		self.set(key, None)
		self.save()

	def get_webhook_secret(self, endpoint="Membership"):
		fieldname = "membership_webhook_secret" if endpoint == "Membership" else "donation_webhook_secret"
		return self.get_password(fieldname=fieldname, raise_exception=False)

@frappe.whitelist()
def get_plans_for_membership(*args, **kwargs):
	controller = get_payment_gateway_controller("Razorpay")
	plans = controller.get_plans()
	return [plan.get("item") for plan in plans.get("items")]
