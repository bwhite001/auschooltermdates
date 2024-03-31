import requests
from datetime import datetime
from collections import defaultdict
from ics import Calendar
import json

URL = "https://www.education.act.gov.au/public-school-life/term_dates_and_public_holidays/ical-feed"


class ACTTermDates:
    """

    ACTTermDates class is a utility class that is used to download data from a specified URL and filter a list of events. The class contains the following methods:

    - __init__(self): Initializes the ACTTermDates class by setting the URL and creating an empty data dictionary. It also calls the download_data() method to download and filter the data
    *.

    - parse_date(date_str): A static method that takes a date string as input and tries to parse it into a datetime object. Returns the parsed datetime object or None if the parsing fails
    *.

    - filter_events(self, events): Filters the given list of events and populates the data dictionary based on the filtered events. The dictionary is structured as follows: {year: {term
    *: {'start': start_date, 'end': end_date}}}

    - download_data(self): Downloads data from the specified URL, filters the events, and returns the filtered data dictionary.

    The class does not return any values, except for the download_data() method which returns the filtered data dictionary.

    """

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

    def filter_events(self, events):
        term_events = []
        for event in events:
            if event.name.startswith("Term"):
                name = event.name.split('-')[0].strip()
                date = event.begin.datetime
                date_type = name.split(' ')[-1].strip()
                year = date.year
                term = name.replace(date_type, '').strip()
                # date = self.parse_date(columns[2])
                if len(self.data_dict[f"{year}"][term]) == 0:
                    self.data_dict[f"{year}"][term] = {}
                if date_type.startswith('Begins'):
                    self.data_dict[f"{year}"][term]['start'] = date.strftime('%Y-%m-%d')
                else:
                    self.data_dict[f"{year}"][term]['end'] = date.strftime('%Y-%m-%d')

    def download_data(self):
        """
        Downloads data from a specified URL and filters the events.

        :return: dictionary of filtered events
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            raw_data = response.content.decode("utf-8")
            cal = Calendar(raw_data)
            events = cal.events
            self.filter_events(events)

        return self.data_dict
