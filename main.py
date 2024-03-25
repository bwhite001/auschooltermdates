import json
import datetime

from TermData import NSWTermDates
from TermData import VICTermDates


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super().default(o)


# Term dates for all states
all_term_dates = {}

# Loop through all states
states = ["NSW", "VIC"]

for state in states:
    term_dates = None
    if state.upper() == "NSW":
        term_dates = NSWTermDates()
    elif state.upper() == "VIC":
        term_dates = VICTermDates()

    # Get the term dates for all years
    if term_dates.data_dict is not None:
        state_term_dates = term_dates.data_dict
        all_term_dates[state] = state_term_dates

# Write the term dates for all states to a JSON file
with open("dist/term_dates.json", "w") as f:
    json.dump(all_term_dates, f, ensure_ascii=False, indent=4, cls=DateTimeEncoder)
