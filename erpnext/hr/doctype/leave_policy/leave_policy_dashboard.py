from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname':  'leave_policy',
		'transactions': [
			{
<<<<<<< HEAD
				'label': _('Employees'),
				'items': ['Employee', 'Employee Grade']
			},
			{
=======
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
				'label': _('Leaves'),
				'items': ['Leave Allocation']
			},
		]
	}	
