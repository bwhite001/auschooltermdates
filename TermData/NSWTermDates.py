import requests
from datetime import datetime
from collections import defaultdict

URL = "https://opendata.transport.nsw.gov.au/dataset/963e4946-46c0-4c9c-b4dc-5033c9e61f5c/resource/66953545-0a91-4a85-92c3-edf46b0f67e3/download/school_day-2019-2025.csv"


class NSWTermDates:

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
            return datetime.strptime(date_str.strip(), '%d/%m/%Y')  # str.strip() will remove lead/trail white spaces
        except ValueError:
            print(f"Unable to parse date: {date_str}")
            return None

    def download_data(self):

        response = requests.get(self.url)

        if response.status_code == 200:
            raw_data = response.content.decode("utf-8")
            split_data = raw_data.split("\n")[1:]

            for row in split_data:
                dates = row.split(',')
                if len(dates[0]) > 0:
                    start_date = self.parse_date(dates[0])
                    end_date = self.parse_date(dates[1])

                    self.data_dict[start_date.year][f"Term {self.get_quarter(start_date)}"] = {
                        'start': start_date.strftime('%Y-%m-%d'),
                        'end': end_date.strftime('%Y-%m-%d'),
                    }

        return self.data_dict
