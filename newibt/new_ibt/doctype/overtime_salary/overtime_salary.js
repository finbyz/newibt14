// Copyright (c) 2022, ibt and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Salary', {
	employee:function(frm){
		if (frm.doc.employee){
			frappe.call({
				method: 'newibt.new_ibt.doctype.overtime_salary.overtime_salary.get_salary_structure_assignment',
				args: {
					employee:frm.doc.employee
				},
				callback: function(r) {
					if(r.message){
						frm.set_value('salary_structure_assignment',r.message)
					}
					else{
						frappe.throw("Please add Salary Structure Assignment for Employee")
					}
				}
			});
		}
	},
	hours:function(frm){
		frappe.model.get_value("Salary Structure Assignment",frm.doc.salary_structure_assignment,'base' ,(r) => {
			let week_amount  = flt(((((r.base/2) * 12) / (365 * 8 ))) * frm.doc.hours);
			if(frm.doc.based_on == 'OT On Weekday'){
				frm.set_value('amount', (week_amount*1.25))
			}
			if(frm.doc.based_on == 'OT On Weekend' || frm.doc.based_on == 'Working On Public Holiday'){
				frm.set_value('amount', (week_amount*1.5))
			}
		})
	},
    based_on:function(frm){
		if (frm.doc.hours){
			frappe.model.get_value("Salary Structure Assignment",frm.doc.salary_structure_assignment,'base' ,(r) => {
				let week_amount  = flt(((((r.base/2) * 12) / (365 * 8 ))) * frm.doc.hours);
				if(frm.doc.based_on == 'OT On Weekday'){
					frm.set_value('amount', (week_amount*1.25))
				}
				if(frm.doc.based_on == 'OT On Weekend' || frm.doc.based_on == 'Working On Public Holiday'){
					frm.set_value('amount', (week_amount*1.5))
				}
			})
		}
	}
});
