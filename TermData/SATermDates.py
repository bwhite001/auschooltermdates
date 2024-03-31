import json
from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re

URL = "https://www.education.sa.gov.au/students/term-dates-south-australian-state-schools#term-dates-across-australia"


class SATermDates:
    def __init__(self):
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download(URL)

    @staticmethod
    def parse_paragraph(term, year):
        start_date_string, break_str, end_date_string = term.contents
        start_date_string = start_date_string.strip().replace(' to', '')
        end_date_string = end_date_string.strip()
        start_date_string += f" {year}"
        end_date_string += f" {year}"
        start_date = datetime.strptime(
            start_date_string, '%d %B %Y')
        end_date = datetime.strptime(
            end_date_string.strip(), '%d %B %Y')

        return {'start': start_date.strftime('%Y-%m-%d'), 'end': end_date.strftime('%Y-%m-%d')}

    def create_soup(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        years = table.find('tbody').find_all('tr')
        for year in years:
            year_text = year.find('th').text.strip()
            terms = list(year.find_all('td'))
            for index, term in enumerate(terms):
                dates = self.parse_paragraph(term, year_text)
                self.data_dict[year_text][f"Term {index + 1}"] = dates

    def download(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.create_soup(response)
