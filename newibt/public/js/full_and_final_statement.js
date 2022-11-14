frappe.ui.form.on('Full and Final Statement', {
	employee:function(frm){
		if (frm.doc.employee){
			frappe.call({
				method: 'newibt.new_ibt.doc_events.full_and_final_statement.get_salary_structure_assignment',
				args: {
					employee:frm.doc.employee
				},
				callback: function(r) {
					frm.set_value('salary_structure_assignment',r.message)
                    console.log(r.message)
				}
			});
		}
	},
});