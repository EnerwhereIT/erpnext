# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'course',
<<<<<<< HEAD
		'non_standard_fieldnames': {
		},
		'transactions': [
			{
				'label': _('Course'),
				'items': ['Course Enrollment', 'Course Schedule']
=======
		'transactions': [
			{
				'label': _('Program and Course'),
				'items': ['Program', 'Course Enrollment', 'Course Schedule']
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
			},
			{
				'label': _('Student'),
				'items': ['Student Group']
			},
			{
				'label': _('Assessment'),
<<<<<<< HEAD
				'items': ['Assessment Plan']
=======
				'items': ['Assessment Plan', 'Assessment Result']
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
			},
		]
	}