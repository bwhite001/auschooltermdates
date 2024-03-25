import requests
from datetime import datetime
from collections import defaultdict

URL = "https://discover.data.vic.gov.au/dataset/a8bc540d-181b-4fb5-8110-5fe52a04f6a7/resource/65c5b668-b230-41d7-9973-a964c8af2ba7/download/dates20file20for20api20feb202019.csv"


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
            split_data = [row for row in raw_data.split("\n") if row.startswith("SCHOOL_TERM,")]

            for row in split_data:
                columns = row.split(',')
                if len(columns) == 6:
                    dateType = columns[1].strip().split('-')[1].strip()
                    term = columns[1].strip().split('-')[0].split(' ')[1:]
                    date = self.parse_date(columns[2])
                    if len(self.data_dict[term[1]][f"Term {term[0]}"]) == 0:
                        self.data_dict[term[1]][f"Term {term[0]}"] = [0, 0]
                    if dateType.startswith('Start'):
                        self.data_dict[term[1]][f"Term {term[0]}"][0] = date
                    else:
                        self.data_dict[term[1]][f"Term {term[0]}"][1] = date

        return self.data_dict


vicDates = VICTermDates()
print(vicDates.data_dict)
