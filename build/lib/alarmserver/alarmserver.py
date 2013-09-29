"""
Created on 23.09.2013
@author: lehmann
"""
from datetime import datetime

SIGNAL_ALARM_RAISED = "alarmRaised(int, QString)"
BIT_COUNT = 16

class AlarmNotDefinedError(Exception):
    pass

class Alarm():
    """
    An instance of this class represents a defined or active alarm

    @ivar alarm_nr: unique alarm number, used as key value
    @type alarm_nr: int

    @ivar text: alarm text
    @type text: basestring

    @ivar time_raised_first: the first time the alarm has been raised
    @type time_raised_first: datetime

    @ivar time_raised_last: the last time the alarm has been raised
    @type time_raised_last: datetime

    @ivar time_acknowledged: time when alarm got acknowledged
    @type time_acknowledged: datetime

    @ivar counter: number of times the alarm has been raised since active
    @type counter: int

    @ivar is_acknowledged: shows if the alarm has been acknowledged
    @type is_acknowledged: bool

    @ivar is_active: shows if the alarm is currently active
    @type is_active: bool
    """
    def __init__(self, alarm_nr, text):
        self.alarm_nr = alarm_nr
        self.text = text
        self.time_coming = None
        self.time_going = None
        self.time_acknowledged = None
        self.counter = 1
        self.is_acknowledged = False
        self.is_active = False
        
    def acknowledge(self):
        """
        Acknowledge the alarm by setting time_acknowledge and the acknowledged property.

        """
        self.time_acknowledged = datetime.now()
        self.is_acknowledged = True

    def clear(self):
        """
        Clear the alarm by setting back all dynamic attributes to the init values.

        """
        self.is_active = False
        self.is_acknowledged = False
        self.time_coming = None
        self.time_going = None
        self.time_acknowledged = None
        self.counter = 1

class AlarmServer():
    """
    An alarm server with the possibility to define alarms, raise, acknowledge and clear them.

    @ivar current_alarms: list of all active alarms, key is the alarm number
    @type current_alarms: list

    @ivar defined_alarms: dictionary of all defined alarms, key is the alarm number
    @type defined_alarms: dict

    """
    def __init__(self):
        self.current_alarms = []
        self.defined_alarms = dict()

    def acknowledge(self, alarm_nr):
        """
        @summary: acknowledges the given alarm
        """
        active_alarm = self.defined_alarms.get(alarm_nr)
        if active_alarm is None:
            return
        active_alarm.acknowledge()
    
    def acknowledge_all(self):
        """
        @summary: acknowledges all active alarms
        """
        for alarm in self.current_alarms:
            alarm.acknowledge()

    def alarm_coming(self, alarm_nr):
        """
        @summary: creates a new alarm object if the alarm number can not be found in active alarms, else the alarm counter
        of the active alarm is increased by 1
        @type alarm_nr: int
        @param alarm_nr: number of the alarm to be raised
        """
        alarm = self.defined_alarms.get(alarm_nr)

        if alarm is None:
            raise AlarmNotDefinedError(alarm_nr)

        if not alarm.is_active:
            alarm.time_coming = datetime.now()
            alarm.is_acknowledged = False
            alarm.time_acknowledged = None

            if alarm in self.current_alarms:
                alarm.counter += 1
            else:
                self.current_alarms.append(alarm)

        alarm.is_active = True

    def alarm_going(self, alarm_nr):
        alarm = self.defined_alarms.get(alarm_nr)
        if alarm is None:
            raise AlarmNotDefinedError(alarm_nr)

        if alarm.is_active:
            alarm.is_active = False
            alarm.time_going = datetime.now()

    def clear(self, alarm_nr):
        """
        @summary: removes the alarm with the given alarm number from the list of active alarms
        """
        active_alarm = self.defined_alarms.get(alarm_nr)
        if active_alarm is not None:
            active_alarm.clear()
            self.current_alarms.remove(active_alarm)

    def clear_all(self):
        """
        Remove all alarms from the list of active alarms.
        """
        while len(self.current_alarms) > 0:
            active_alarm = self.current_alarms[0]
            self.clear(active_alarm.alarm_nr)

    def define_alarm(self, alarm_nr, alarm_text):
        """
        @summary: defines a new alarm and adds it to the defined alarms
        """
        alarm = Alarm(alarm_nr, alarm_text)
        self.defined_alarms[alarm_nr] = alarm

    @property
    def unacknowledged_alarms(self):
        retVal = []
        for active_alarm in self.current_alarms:
            if not active_alarm.is_acknowledged:
                retVal.append(active_alarm)
        return retVal


def bit_of_word(word, index):
    """
    @summary: returns the bit value of the word on the digit place given by index
    """
    return (word >> index) & 1 == 1

