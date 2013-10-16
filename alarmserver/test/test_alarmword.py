
__author__ = 'lehmann'

import unittest

from alarmserver.alarmserver import AlarmWord, bit_value, AlarmNotDefinedError, Alarm
from alarmserver.gui import AlarmServerModel

class MyAlarmWord(AlarmWord):
    def __init__(self, alarmserver):
        AlarmWord.__init__(self, alarmserver)

        self.alarmserver.define_alarm(0, u"Fehler 0")
        self.alarmserver.define_alarm(1, u"Fehler 1")
        self.alarmserver.define_alarm(2, u"Fehler 2")

class TestAlarmWord(unittest.TestCase):

    def setUp(self):
        self.alarmserverModel = AlarmServerModel()
        self.alarm_word = MyAlarmWord(self.alarmserverModel)

    def test_bit_value(self):
        word= int("0110", 2)
        self.assertEqual(bit_value(word, 0), False)
        self.assertEqual(bit_value(word, 1), True)
        self.assertEqual(bit_value(word, 2), True)
        self.assertEqual(bit_value(word, 3), False)

    def test_alarm_not_define_error(self):
        def helper_function():
            self.alarm_word.value = int("1010", 2)
        self.assertRaises(AlarmNotDefinedError, helper_function)

    def test_alarm_coming_and_going(self):
        self.alarm_word.value=int("10", 2)
        alarm = self.alarmserverModel.current_alarms[0]
        self.assertTrue(alarm.is_active)

        self.alarm_word.value=int("0", 2)
        alarm = self.alarmserverModel.current_alarms[0]
        self.assertFalse(alarm.is_active)


