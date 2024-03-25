import requests
from datetime import datetime
from collections import defaultdict
from ics import Calendar

URL = "https://content.vic.gov.au/sites/default/files/2021-12/Victorian-school-term-dates.ics"


class VICTermDates:

    def __init__(self):
        self.url = URL
        self.data_dict = defaultdict(lambda: defaultdict(list))
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
            raw_data = response.content.decode("utf-8")
            c = Calendar(raw_data)

            # for row in split_data:
            #     columns = row.split(',')
            #     if len(columns) == 6:
            #         dateType = columns[1].strip().split('-')[1].strip()
            #         term = columns[1].strip().split('-')[0].split(' ')[1:]
            #         date = self.parse_date(columns[2])
            #         if len(self.data_dict[term[1]][f"Term {term[0]}"]) == 0:
            #             self.data_dict[term[1]][f"Term {term[0]}"] = [0, 0]
            #         if dateType.startswith('Start'):
            #             self.data_dict[term[1]][f"Term {term[0]}"][0] = date.strftime('%Y-%m-%d')
            #         else:
            #             self.data_dict[term[1]][f"Term {term[0]}"][1] = date.strftime('%Y-%m-%d')

        return self.data_dict
