import json
from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re

URL = "https://education.qld.gov.au/about-us/calendar/term-dates"
FUTURE_URL = "https://education.qld.gov.au/about-us/calendar/future-dates"

class QLDTermDates:

    def __init__(self):
        self.url = URL
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download_data()

    @staticmethod
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

    def parseCurent(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        year = soup.find('h3', string="Queensland term dates").find_previous("h2").text.strip()
        h3 = soup.find('h3', string="Queensland term dates")
        # find the next 4 strong elements containing 'Term'
        terms = h3.find_all_next('strong', string=re.compile('^Term'))[:4]
        for term in terms:
            term_text = term.text.strip()
            dates = self.parse_paragraph(term.parent.text, year)
            self.data_dict[year][term_text] = dates

    def download_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.parseCurent(response)
        return self.data_dict

test = QLDTermDates()
print(json.dumps(test.data_dict, indent=2))