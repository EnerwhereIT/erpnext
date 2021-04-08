# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'assessment_plan',
<<<<<<< HEAD
		'non_standard_fieldnames': {
		},
=======
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
		'transactions': [
			{
				'label': _('Assessment'),
				'items': ['Assessment Result']
			}
<<<<<<< HEAD
=======
		],
		'reports': [
			{
				'label': _('Report'),
				'items': ['Assessment Plan Status']
			}
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
		]
	}