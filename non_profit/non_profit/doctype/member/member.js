// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Member', {
	setup: function (frm) {
		frappe.db.get_single_value('Non Profit Settings', 'enable_razorpay_for_memberships').then(val => {
			if (val && (frm.doc.subscription_id || frm.doc.customer_id)) {
				frm.set_df_property('razorpay_details_section', 'hidden', false);
			}
		})
	},
	refresh: function (frm) {

		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Member' };

		frm.toggle_display(['address_html', 'contact_html'], !frm.doc.__islocal);

		if (!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function () {
				if (frm.doc.customer) {
					frappe.set_route('query-report', 'General Ledger', { party_type: 'Customer', party: frm.doc.customer });
				} else {
					frappe.set_route('query-report', 'General Ledger', { party_type: 'Member', party: frm.doc.name });
				}
			});

			frm.add_custom_button(__('Accounts Receivable'), function () {
				frappe.set_route('query-report', 'Accounts Receivable', { customer: frm.doc.customer });
			});

			if (!frm.doc.customer) {
				frm.add_custom_button(__('Create Customer'), () => {
					frm.call('make_customer_and_link').then(() => {
						frm.reload_doc();
					});
				});
			}

			// indicator
			erpnext.utils.set_party_dashboard_indicators(frm);

		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}

		// frappe.call({
		// 	method: "frappe.client.get_value",
		// 	args: {
		// 		'doctype': "Membership",
		// 		'filters': { 'member': frm.doc.name },
		// 		'fieldname': [
		// 			'to_date'
		// 		]
		// 	},
		// 	callback: function (data) {
		// 		if (data.message) {
		// 			frappe.model.set_value(frm.doctype, frm.docname,
		// 				"membership_expiry_date", data.message.to_date);
		// 		}
		// 	}
		// });
	}
});

// function create_contact_and_address(frm) {
// 	// Create Contact
// 	frappe.call({
// 		method: "frappe.client.insert",
// 		args: {
// 			doc: {
// 				doctype: "Contact",
// 				first_name: frm.doc.rep_name,
// 				email_id: frm.doc.email_id,
// 				phone: frm.doc.phone,
// 				links: [{
// 					link_doctype: "Member",
// 					link_name: frm.doc.name
// 				}]
// 			}
// 		},
// 		callback: function (response) {
// 			frappe.msgprint(__('Contact created successfully'));

// 			// Create Address after Contact is created
// 			frappe.call({
// 				method: "frappe.client.insert",
// 				args: {
// 					doc: {
// 						doctype: "Address",
// 						address_title: frm.doc.rep_name,
// 						county: frm.doc.county,
// 						address_line1: "Address Line 1",
// 						city: "City",
// 						links: [{
// 							link_doctype: "Member",
// 							link_name: frm.doc.name
// 						}]
// 					}
// 				},
// 				callback: function (response) {
// 					frappe.msgprint(__('Address created successfully'));

// 					// Update HTML fields and set flag
// 					var contact_html = "Email: " + frm.doc.email_id + "<br>Representative Email: " + frm.doc.representative_email_id + "<br>Phone: " + frm.doc.phone;
// 					var address_html = "County: " + frm.doc.county;

// 					frappe.db.set_value('Member', frm.doc.name, {
// 						'contact_html': contact_html,
// 						'address_html': address_html,
// 						'contact_and_address_created': 1
// 					}).then(() => {
// 						frappe.msgprint(__('HTML fields updated and flag set.'));
// 						frm.reload_doc();
// 						frm.save()
// 					});
// 				}
// 			});
// 		}
// 	});
// }