import json
import datetime
import os
from TermData import *
from TermData.SATermDates import SATermDates
from TermData.TASTermDates import TASTermDates

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super().default(o)


def run():
    all_term_dates = {}

    states = {
        'ACT': ACTTermDates(),
        'NSW': NSWTermDates(),
        'NT': NTTermDates(),
        'QLD': QLDTermDates(),
        'SA': SATermDates(),
        'TAS': TASTermDates(),
        'VIC': VICTermDates(),
        'WA': WATermDates()
    }

    for state, term_dates in states.items():
        if term_dates.data_dict is not None:
            state_term_dates = term_dates.data_dict
            all_term_dates[state] = state_term_dates

    if not os.path.exists("dist"):
        os.makedirs("dist")

    with open("dist/term_dates.json", "w") as f:
        json.dump(all_term_dates, f, ensure_ascii=False, indent=4, cls=DateTimeEncoder)


if __name__ == "__main__":
    run()