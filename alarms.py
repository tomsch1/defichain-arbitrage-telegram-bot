import json
from datetime import datetime, timedelta
import os

from crypto_comparison import CryptoComparison
from stock_token_comparison import StockComparison


class Alarm():

    def __init__(self, symbol: str, threshold: float, callback_ref: str):
        self.symbol_name = symbol
        self.threshold = threshold
        self.last_alerted = None
        self.callback_ref = callback_ref


    def dict(self):
        return {"symbol_name": self.symbol_name, "threshold": self.threshold, "callback_ref": self.callback_ref}


class AlarmsConfig:

    def __init__(self, database_path: str):
        self.database_path = database_path
        self.active_alarms = []
        self.load_from_json()


    def add_alarm(self, alarm: Alarm):
        #if already existing
        for active_alarm in self.active_alarms:
            if (active_alarm.callback_ref == alarm.callback_ref and
               active_alarm.symbol_name == alarm.symbol_name):
                self.active_alarms.remove(active_alarm)
        self.active_alarms.append(alarm)
        self.save_to_json()

    def save_to_json(self):
        with open(self.database_path, "w") as file:
            to_dump = [alarm.dict() for alarm in self.active_alarms]
            json.dump(to_dump, file)

    def load_from_json(self):
        if os.path.isfile(self.database_path):
            with open(self.database_path, "r") as file:
                for jsonObj in file:
                    list_of_alarm_dicts = json.loads(jsonObj)
                    for alarm in list_of_alarm_dicts:
                        alarm = Alarm(alarm["symbol_name"], alarm["threshold"], alarm["callback_ref"])
                        self.active_alarms.append(alarm)
        else: print(f"{self.database_path} file does not exists")


class StockAlarmConfig:

    def __init__(self, stock_token_comparison: StockComparison, alarm_database_path: str):
        self.stock_comparison = stock_token_comparison
        self.alarmsConfig = AlarmsConfig(alarm_database_path)

    def evaluate_list_alarms(self, ):
        triggered_alarm_list = []
        now_minus_two_miuntes = datetime.now() - timedelta(minutes=60)
        for alarm in self.alarmsConfig.active_alarms:
            alarm_pair = self.stock_comparison.evaluate_alarm(alarm.symbol_name, alarm.threshold)
            if alarm_pair is not None:
                if alarm.last_alerted is None:
                    alarm.last_alerted = datetime.now()
                    triggered_alarm_list.append({alarm.callback_ref: alarm_pair})
                elif alarm.last_alerted < now_minus_two_miuntes:
                    alarm.last_alerted = datetime.now()
                    triggered_alarm_list.append({alarm.callback_ref: alarm_pair})
        return triggered_alarm_list


class CryptoAlarmConfig:

    def __init__(self, crypto_comparison: CryptoComparison, alarm_database_path: str):
        self.crypto_comparison = crypto_comparison
        self.alarmsConfig = AlarmsConfig(alarm_database_path)

    def evaluate_list_alarms(self, ):
        triggered_alarm_list = []
        now_minus_two_miuntes = datetime.now() - timedelta(minutes=60)
        for alarm in self.alarmsConfig.active_alarms:
            alarm_pair = self.crypto_comparison.evaluate_alarm(alarm.symbol_name, alarm.threshold)
            if alarm_pair is not None:
                if alarm.last_alerted is None:
                    alarm.last_alerted = datetime.now()
                    triggered_alarm_list.append({alarm.callback_ref: alarm_pair})
                elif alarm.last_alerted < now_minus_two_miuntes:
                    alarm.last_alerted = datetime.now()
                    triggered_alarm_list.append({alarm.callback_ref: alarm_pair})
        return triggered_alarm_list
