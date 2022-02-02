import frappe

from frappe import _, scrub
from frappe.utils.data import comma_or
from erpnext.erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from erpnext.erpnext.accounts.doctype.invoice_discounting.invoice_discounting import \
	get_party_account_based_on_invoice_discounting


class NonProfitPaymentEntry(PaymentEntry):
	def set_party_type(dt):
		if dt in ("Sales Invoice", "Sales Order", "Dunning"):
			party_type = "Customer"
		elif dt in ("Purchase Invoice", "Purchase Order"):
			party_type = "Supplier"
		elif dt in ("Expense Claim", "Employee Advance"):
			party_type = "Employee"
		elif dt == "Fees":
			party_type = "Student"
		elif dt == "Donation":
			party_type = "Donor"
		return party_type

	def validate_reference_documents(self):
		if self.party_type == "Student":
			valid_reference_doctypes = ("Fees")
		elif self.party_type == "Customer":
			valid_reference_doctypes = ("Sales Order", "Sales Invoice", "Journal Entry", "Dunning")
		elif self.party_type == "Supplier":
			valid_reference_doctypes = ("Purchase Order", "Purchase Invoice", "Journal Entry")
		elif self.party_type == "Employee":
			valid_reference_doctypes = ("Expense Claim", "Journal Entry", "Employee Advance")
		elif self.party_type == "Shareholder":
			valid_reference_doctypes = ("Journal Entry")
		elif self.party_type == "Donor":
			valid_reference_doctypes = ("Donation")

		for d in self.get("references"):
			if not d.allocated_amount:
				continue
			if d.reference_doctype not in valid_reference_doctypes:
				frappe.throw(_("Reference Doctype must be one of {0}")
					.format(comma_or(valid_reference_doctypes)))
			elif d.reference_name:
				if not frappe.db.exists(d.reference_doctype, d.reference_name):
					frappe.throw(_("{0} {1} does not exist").format(d.reference_doctype, d.reference_name))
				else:
					ref_doc = frappe.get_doc(d.reference_doctype, d.reference_name)
					if d.reference_doctype != "Journal Entry":
						if self.party != ref_doc.get(scrub(self.party_type)):
							frappe.throw(_("{0} {1} is not associated with {2} {3}")
								.format(d.reference_doctype, d.reference_name, self.party_type, self.party))
					else:
						self.validate_journal_entry()
					if d.reference_doctype in ("Sales Invoice", "Purchase Invoice", "Expense Claim", "Fees"):
						if self.party_type == "Customer":
							ref_party_account = get_party_account_based_on_invoice_discounting(d.reference_name) or ref_doc.debit_to
						elif self.party_type == "Student":
							ref_party_account = ref_doc.receivable_account
						elif self.party_type=="Supplier":
							ref_party_account = ref_doc.credit_to
						elif self.party_type=="Employee":
							ref_party_account = ref_doc.payable_account
						if ref_party_account != self.party_account:
								frappe.throw(_("{0} {1} is associated with {2}, but Party Account is {3}")
									.format(d.reference_doctype, d.reference_name, ref_party_account, self.party_account))
					if ref_doc.docstatus != 1:
						frappe.throw(_("{0} {1} must be submitted")
							.format(d.reference_doctype, d.reference_name))

