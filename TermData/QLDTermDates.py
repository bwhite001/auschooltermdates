from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from ics import Calendar
import json
from bs4 import BeautifulSoup

URL = "https://education.qld.gov.au/about-us/calendar/term-dates"


def parse_paragraph(text, year):
    text = text.split('—')[0]  # remove the part that is not needed
    start_date_string, end_date_string = text.split(
        'to')  # split start and end dates
    start_date_string = start_date_string.split(
        ':')[1].strip()  # remove 'Term 1:' part
    start_date_string += f" {year}"
    end_date_string += f" {year}"
    start_date = datetime.strptime(
        start_date_string, '%A %d %B %Y')  # convert string to date
    end_date = datetime.strptime(
        end_date_string.strip(), '%A %d %B %Y')  # convert string to date

    return {'start': start_date.strftime('%Y-%m-%d'), 'end': end_date.strftime('%Y-%m-%d')}


class QLDTermDates:

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
            # str.strip() will remove lead/trail white spaces
            return datetime.strptime(date_str.strip(), '%Y-%m-%d')
        except ValueError:
            print(f"Unable to parse date: {date_str}")
            return None

    def download_data(self):

        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            year = soup.find('h3', string="Queensland term dates").find_previous("h2").text.strip()
            terms = ['Term 1', 'Term 2', 'Term 3', 'Term 4']
            for term in terms:
                raw_data = soup.find('strong', string=term)
                if raw_data:
                    dates = parse_paragraph(raw_data.parent.text, year)
                    self.data_dict[year][term] = dates
        return self.data_dict
