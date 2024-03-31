import json
import datetime
from TermData import *
from TermData.SATermDates import SATermDates


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder class for encoding datetime objects.

        This class inherits from the `json.JSONEncoder` class and provides custom encoding for datetime objects. When encoding a datetime object, it converts it to its ISO 8601 string representation
    *.

        Args:
            json.JSONEncoder: The base class for JSON encoders.

        Methods:
            default: Overrides the default method from the base class to provide custom encoding for datetime objects.

        Example:
            import json
            import datetime

            class DateTimeEncoder(json.JSONEncoder):
                def default(self, o):
                        if isinstance(o, datetime.datetime):
                            return o.isoformat()

                        return super().default(o)
        """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super().default(o)


def run():
    """
    Collects and writes the term dates for all states to a JSON file.

    :return: None
    """
    # Term dates for all states
    all_term_dates = {}

    # Loop through all states
    states = {
        'ACT': ACTTermDates(),
        'NSW': NSWTermDates(),
        'QLD': QLDTermDates(),
        'SA': SATermDates(),
        'VIC': VICTermDates(),
        'WA': WATermDates()
    }

    for state, term_dates in states.items():
        # Get the term dates for all years
        if term_dates.data_dict is not None:
            state_term_dates = term_dates.data_dict
            all_term_dates[state] = state_term_dates

    # Write the term dates for all states to a JSON file
    with open("dist/term_dates.json", "w") as f:
        json.dump(all_term_dates, f, ensure_ascii=False, indent=4, cls=DateTimeEncoder)


if __name__ == "__main__":
    run()
