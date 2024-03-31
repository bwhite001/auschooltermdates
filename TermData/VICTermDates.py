import requests
from datetime import datetime
from collections import defaultdict
from ics import Calendar
import json

URL = "https://content.vic.gov.au/sites/default/files/2021-12/Victorian-school-term-dates.ics"


class VICTermDates:

    def __init__(self):
        self.url = URL
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download_data()

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d')  # str.strip() will remove lead/trail white spaces
        except ValueError:
            print(f"Unable to parse date: {date_str}")
            return None

    def download_data(self):

        response = requests.get(self.url)

        if response.status_code == 200:
            raw_data = response.content.decode("utf-8")
            cal = Calendar(raw_data)
            events = cal.events
            for event in events:
                if 'government' in event.name:
                    continue
                date = event.begin.datetime
                date_type = event.name.strip().split(' ')[-1]
                year = date.year
                term = event.name.replace(date_type, '').strip()
                # date = self.parse_date(columns[2])
                if len(self.data_dict[f"{year}"][term]) == 0:
                    self.data_dict[f"{year}"][term] = {}
                if date_type.startswith('starts'):
                    self.data_dict[f"{year}"][term]['start'] = date.strftime('%Y-%m-%d')
                else:
                    self.data_dict[f"{year}"][term]['end'] = date.strftime('%Y-%m-%d')

        return self.data_dict
