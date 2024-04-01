import json
from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re

URL = "https://nt.gov.au/learning/primary-and-secondary-students/school-term-dates-in-nt"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}


class NTTermDates:
    def __init__(self):
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download(URL)

    @staticmethod
    def parse_paragraph(text, year):
        start_date_string, end_date_string = text.split('|')
        start_date_string = start_date_string.strip()
        end_date_string = end_date_string.strip()
        start_date_string += f" {year}"
        end_date_string += f" {year}"
        start_date = datetime.strptime(
            start_date_string, '%A %d %B %Y')
        end_date = datetime.strptime(
            end_date_string.strip(), '%A %d %B %Y')

        return {'start': start_date.strftime('%Y-%m-%d'), 'end': end_date.strftime('%Y-%m-%d')}

    def create_soup(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        year_container = soup.find_all('table')
        self.parse_soup(year_container)

    def parse_soup(self, years):
        for index, year_table in enumerate(years):
            if index == 0:
                year_text = year_table.find_previous('h2').text.strip().split(' ')[0].strip()
            else:
                year_text = year_table.find_previous('h3').text.strip()

            terms = year_table.find_all('tr')[1:]
            for term in terms:
                term_text = term.find('th').text.strip()
                term_text = re.sub(r'\s', ' ', term_text)
                start_date, end_date = term.find_all('td')
                if start_date.find('p') is not None:
                    start_date = start_date.find('p').text.strip()
                else:
                    start_date = start_date.text.strip()
                end_date = end_date.text.strip()
                dates = self.parse_paragraph(f"{start_date}|{end_date}", year_text)
                self.data_dict[year_text][term_text] = dates

    def download(self, url):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            self.create_soup(response)


nt = NTTermDates()
print(json.dumps(nt.data_dict, indent=2))
