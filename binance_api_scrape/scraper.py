import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import requests
from typing import Union, Dict, List


ENDPOINTS = {
    'ping': '/vapi/v1/ping',
    'time': '/vapi/v1/time',
    'optionInfo': '/vapi/v1/optionInfo',
    'mark': '/vapi/v1/mark',
    'ticker': '/vapi/v1/ticker',
}

def ts(timestamp):
    return datetime.fromtimestamp(int(timestamp / 1e3))


def return_data(json):
    if not json['code']:
        return json['data']
    else:
        return json['msg']


def server_time(f):
    def func(*args, **kwargs):
        date = args[0].ts()
        return {'ts': date, 'data': f(*args, **kwargs)}
    return func


@dataclass
class Scraper:
    base_url = "https://vapi.binance.com"
    endpoints = ENDPOINTS
    tz = "Europe/Paris"

    def fetch_json(self, suffix, params=None) -> Union[List, Dict, str]:
        response = requests.get(self.base_url + suffix, params)
        json = response.json()
        return return_data(json)

    def ping(self):
        response = requests.get(self.base_url + self.endpoints['ping'])
        return response.json()['msg']


    def time(self):
        return self.fetch_json(self.endpoints['time'])

    def ts(self):
        return pd.Timestamp(self.date(), tz=self.tz)

    def date(self):
        return ts(self.time())

    @server_time
    def option_info(self):
        return self.fetch_json(self.endpoints['optionInfo'])

    @server_time
    def mark(self, symbol=None):
        params = {'symbol': symbol}
        return self.fetch_json(self.endpoints['mark'], params)

    @server_time
    def ticker(self, symbol=None):
        params = {'symbol': symbol}
        return self.fetch_json(self.endpoints['ticker'], params)