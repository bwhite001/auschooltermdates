import json
from typing import Dict

import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re

URL = "https://www.education.wa.edu.au/future-term-dates"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}


class WATermDates:
    def __init__(self):
        self.data_dict = defaultdict(lambda: defaultdict(dict))
        self.download(URL)

    @staticmethod
    def parse_paragraph(text, year):
        if len(text.split('to ')) == 2:
            start_date_string, end_date_string = text.split('to ')
        elif len(text.split(' to ')) == 2:
            start_date_string, end_date_string = text.split(' to ')
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
        year_container = soup.find_all('div', class_='eds-c-content-view')
        filtered_year_container = []

        for tag in year_container:
            if tag.contents[1].name == 'h4':
                filtered_year_container.append(tag)
        self.parse_soup(filtered_year_container)

    def parse_soup(self, years):
        for year_tag in years:
            year = year_tag.contents[1].text.split(' ')[0]
            if len(year) != 4 and len(year_tag.contents[1].text.split(' ')[0]) == 4:
                year = year_tag.contents[1].text.split(' ')[0]
            semesters = year_tag.find_all("table")
            for semester in semesters:
                terms = semester.find_all('td', string=re.compile(r'^Term'))
                for term in terms:
                    term_text = term.text.strip()
                    dates = self.parse_paragraph(term.parent.find_all('td')[1].text, year)
                    self.data_dict[year][term_text] = dates

    def download(self, url):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            self.create_soup(response)
