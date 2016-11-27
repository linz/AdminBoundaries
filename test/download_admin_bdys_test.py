
'''
v.0.0.1

download_admin_bdys_test.py

Copyright 2011 Crown copyright (c)
Land Information New Zealand and the New Zealand Government.
All rights reserved

This program is released under the terms of the new BSD license. See the 
LICENSE file for more information.

Tests classes in download_admin_bdys.py

Created on 09/11/2016

@author: jramsay
'''

import unittest
import inspect
import sys
import re
import sys
import os

sys.path.append('../scripts')

from download_admin_bdys import ColumnMapper
from download_admin_bdys import ConfReader
from download_admin_bdys import Version

#testlog = Logger.setup('test')

#user to init an address, simple text string read from a stored config file
user_text = 'aims_user'

class Test00_ConfReader(unittest.TestCase):
	
	def setUp(self):
		self.testdata = '["test1","test2"]'
		self.testname = 'test'
		self.cr = ConfReader()
		
	def tearDown(self):
		self.cr = None
	
	def test00_selfTest(self):
		'''Self tests making sure reader object is instantated correctly'''
		self.assertIsNotNone(self.cr, 'Failied to instantiale reader')
		self.assertIsNotNone(self.cr.parser, 'Failied to instantiale parser')
		
	def test10_save(self):
		'''Tests saving data to config without returning an error'''
		self.assertIsNone(self.cr.save(self.testname,self.testdata),'Save method returns non null value or error')
		
		
	def test20_read(self):
		'''Tests retrieval of data from config file'''
		self.assertEqual(self.testdata,self.cr.read(self.testname,flush=False),"Fetched data does not match saved data")
		self.assertEqual(self.testdata,self.cr.read(self.testname,flush=True),"Fetched data does not match saved data")
		self.assertEqual((),self.cr.read(self.testname,flush=True),"Fetched data should be empty after a flush")
		
class Test10_ColumnMapper(unittest.TestCase):
	
	def setUp(self):
		self.cm = ColumnMapper(ConfReader())	
	
	def tearDown(self):
		pass	
	
	def test00_selfTest(self):
		'''Self tests making sure reader object is instantated correctly'''
		self.assertIsNotNone(self.cm, 'Failied to instantiale mapper')
		self.assertIsNotNone(self.cm.schema, 'Failied to instantiale schema')
		self.assertIsNotNone(self.cm.map, 'Failied to instantiale map')

	def test10_flatten(self):
		'''Tests list flattening function'''
		f1 = [[1,11],[2,[3,33],[4,44],5,[6]],7]
		f2 = [1,11,2,3,33,4,44,5,6,7]
		self.assertEqual(f2,self.cm.flatten(f1))
				
	def test20_action(self):
		'''Tests query generation by matching query string length against known as a sig test'''
		actions = {'add':0,'drop':82,'rename':162,'cast':0,'primary':75,'trans':189}
		for a in actions:
			self.assertEqual(actions[a],sum([len(i) for i in self.cm.action("meshblock","statsnz_meshblock",a)]))
			
					
	def test30_fromqry(self):
		a = ['ALTER TABLE admin_bdys_import.temp_statsnz_meshblock ADD COLUMN A A']
		b = ['ALTER TABLE admin_bdys_import.temp_statsnz_meshblock DROP COLUMN IF EXISTS B']
		c = ['ALTER TABLE admin_bdys_import.temp_statsnz_meshblock ALTER COLUMN C SET DATA TYPE C']
		d = ['ALTER TABLE admin_bdys_import.temp_statsnz_meshblock RENAME COLUMN D TO D']
		e = ["SELECT UpdateGeometrySRID('admin_bdys_import','temp_statsnz_meshblock', 'shape', 4167)", 
			'UPDATE admin_bdys_import.temp_statsnz_meshblock SET shape = ST_Transform(shape::geometry,4167::integer)']
		f = ['ALTER TABLE admin_bdys_import.temp_statsnz_meshblock ADD PRIMARY KEY (code)']
		self.assertEqual(a, self.cm.formqry('add','meshblock','statsnz_meshblock',{'add':'A','type':'A'}))
		self.assertEqual(b, self.cm.formqry('drop','meshblock','statsnz_meshblock','B'))
		self.assertEqual(c, self.cm.formqry('cast','meshblock','statsnz_meshblock',{'cast':'C','type':'C'}))
		self.assertEqual(d, self.cm.formqry('rename','meshblock','statsnz_meshblock',{'old':'D','new':'D'}))
		self.assertEqual(e, self.cm.formqry('trans','meshblock','statsnz_meshblock',None))
		self.assertEqual(f, self.cm.formqry('primary','meshblock','statsnz_meshblock',None))
	
class Test20_Version(unittest.TestCase):
	
	def setUp(self):
		c = ConfReader()
		m = ColumnMapper(c)
		v = Version(c, m)
	
	def tearDown(self):
		pass
	
class Test30_Processor(unittest.TestCase):
	
	def setUp(self):
		c = ConfReader()
		m = ColumnMapper(c)
		v = Version(c, m)
	
	def tearDown(self):
		pass
	
def suite():
	test_suite = unittest.TestSuite()
	test_suite.addTest(unittest.makeSuite(Test00_ConfReader,Test10_ColumnMapper,Test20_Version))
	return test_suite


if __name__ == "__main__":
	unittest.main()