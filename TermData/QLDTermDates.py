import requests
from datetime import datetime
from collections import defaultdict
from ics import Calendar
import json
from bs4 import BeautifulSoup

URL = "https://education.qld.gov.au/about-us/calendar/term-dates"


class VICTermDates:

    def __init__(self):
        self.url = URL
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download_data()

    @staticmethod
    def get_quarter(dt):
        return (dt.month - 1) // 3 + 1

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
            soup = BeautifulSoup(response.text, 'html.parser')

            terms = ['Term 1', 'Term 2', 'Term 3', 'Term 4']
            for term in terms:
                raw_data = soup.find('p', string=term)
                if raw_data:
                    # data processing with raw_data
                    pass

