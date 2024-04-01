import json
from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re

URL = "https://www.decyp.tas.gov.au/learning/term-dates/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}


class TASTermDates:
    def __init__(self):
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download(URL)

    @staticmethod
    def parse_paragraph(seperator, text, year, date_format='%d %B %Y'):
        start_date_string, end_date_string = text.split(seperator)
        start_date_string = start_date_string.strip()
        end_date_string = end_date_string.strip()
        start_date_string += f" {year}"
        end_date_string += f" {year}"
        start_date = datetime.strptime(
            start_date_string, date_format)
        end_date = datetime.strptime(
            end_date_string.strip(), date_format)

        return {'start': start_date.strftime('%Y-%m-%d'), 'end': end_date.strftime('%Y-%m-%d')}

    def create_soup(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        year_elems = soup.find_all('h2', string=re.compile(r'\b\d{4}\b School term dates.*'))
        for index, year_elem in enumerate(year_elems):
            current_year = year_elem.text.strip()
            match = re.search(r'\b\d{4}\b', current_year)
            year = ''
            if match:
                year = match.group(0)
            terms = ['Term 1', 'Term 2', 'Term 3', 'Term 4']
            for term in terms:
                find = 'h3' if (index == 0) else 'strong'
                elm_find = year_elem.parent.find(find, string=re.compile(f'{term}.*'))
                if index == 0:

                    self.parse_current(elm_find, term, year)
                else:
                    self.parse_new(elm_find, term, year)

    def parse_new(self, strong_elm, term, year):
        if strong_elm is not None:
            date_string = strong_elm.parent.contents[1].strip()
            dates = self.parse_paragraph(' to ', date_string, year, '%A %d %B %Y')
            self.data_dict[year][term] = dates

    def parse_current(self, term_elm, term, year):
        if term_elm is not None:
            date_string = term_elm.parent.find('p').text.strip()
            dates = self.parse_paragraph(' – ', date_string, year)
            self.data_dict[year][term] = dates

    def download(self, url):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            self.create_soup(response)
