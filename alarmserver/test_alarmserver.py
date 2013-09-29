#-*- coding: utf-8 -*-
"""
Created on 24.09.2013
@author: lehmann
"""

import unittest
from alarmserver import *

class TestAlarmServer (unittest.TestCase):
    def setUp(self):
        self.server = AlarmServer()
        self.server.define_alarm(0, "alarm 1")
        self.server.define_alarm(1, "alarm 2")
        self.server.define_alarm(2, "alarm 3")
    
    def test_define_alarm(self):
        self.assertEqual(len(self.server.defined_alarms), 3)
        self.assertEqual(self.server.defined_alarms[0].text, "alarm 1")
        self.assertEqual(self.server.defined_alarms[1].text, "alarm 2")
        self.assertEqual(self.server.defined_alarms[2].text, "alarm 3")
        
    def test_raise_alarm(self):
        self.server.alarm_coming(0)
        self.assertEqual(len(self.server.current_alarms), 1)
        self.assertTrue(len(self.server.current_alarms)>0)
        self.assertTrue(self.server.unacknowledged_alarms)
        
    def test_acknowledge(self):
        self.server.alarm_coming(0)
        self.server.alarm_coming(1)
        self.server.acknowledge(0)
        
        self.assertTrue(self.server.current_alarms[0].is_acknowledged)
        self.assertFalse(self.server.current_alarms[1].is_acknowledged)
        self.assertTrue(self.server.unacknowledged_alarms)
        
        self.server.acknowledge(1)
        self.assertTrue(self.server.current_alarms[1].is_acknowledged)
        self.assertFalse(self.server.unacknowledged_alarms)
        
    def test_clear(self):
        self.server.alarm_coming(0)
        self.server.alarm_coming(1)
        
        self.assertEqual(len(self.server.current_alarms), 2)
        self.server.clear(0)
        self.assertEqual(len(self.server.current_alarms), 1)
    
    def test_clear_all(self):
        self.server.alarm_coming(0)
        self.server.alarm_coming(1)
        
        self.assertEqual(len(self.server.current_alarms), 2)
        
        self.server.clear_all()
        
        self.assertEqual(len(self.server.current_alarms), 0)

    def test_raise_alarm_error(self):
        self.assertRaises(Exception, self.server.alarm_coming, 4)
            
    def test_bit_of_word(self):
        for i in range(BIT_COUNT):
            testword = 1<<i
            for j in range(BIT_COUNT):
                if j==i:                                
                    self.assertTrue(bit_of_word(testword, j))
                else:
                    self.assertFalse(bit_of_word(testword, j))

if __name__=="__main__":
    unittest.main(verbosity=2)