# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from erpnext.projects.doctype.task.test_task import create_task

class TestProjectTemplate(unittest.TestCase):
	pass

def make_project_template(project_template_name, project_tasks=[]):
	if not frappe.db.exists('Project Template', project_template_name):
		project_tasks = project_tasks or [
				create_task(subject="_Test Template Task 1", is_template=1, begin=0, duration=3),
				create_task(subject="_Test Template Task 2", is_template=1, begin=0, duration=2),
			]
		doc = frappe.get_doc(dict(
			doctype = 'Project Template',
			name = project_template_name
		))
		for task in project_tasks:
			doc.append("tasks",{
				"task": task.name
			})
		doc.insert()

<<<<<<< HEAD
	return frappe.get_doc('Project Template', 'Test Project Template')

def make_project_template(project_template_name, project_tasks=[]):
	if not frappe.db.exists('Project Template', project_template_name):
		frappe.get_doc(dict(
			doctype = 'Project Template',
			name = project_template_name,
			tasks = project_tasks or [
				dict(subject='Task 1', description='Task 1 description',
					start=0, duration=3),
				dict(subject='Task 2', description='Task 2 description',
					start=0, duration=2),
				dict(subject='Task 3', description='Task 3 description',
					start=2, duration=4),
				dict(subject='Task 4', description='Task 4 description',
					start=3, duration=2),
			]
		)).insert()

=======
>>>>>>> e0222723f05d730463d741de7a5ebff9e2081b3a
	return frappe.get_doc('Project Template', project_template_name)