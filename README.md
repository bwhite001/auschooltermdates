# Australian School Term Dates

This project is a Python application that uses an open data file to provide school term dates for all states and territories in Australia, from 2019 to 2025. It works by downloading a CSV file from the open data website, parsing the CSV file, and printing the term dates in a human-readable format.

## Usage

To use the application, run the provided script. It will download the data and print the school term dates to the console.

The main component of this application is the `NSWTermDates` class. An `NSWTermDates` object requires a URL to initialize, which is where it will download the term data from. The object has several methods to parse and present the data.

## Data Details
The data used in this project is downloaded from an open data directory. The directory provides a series of term dates for different educational periods across all states and territories in Australia. The data specifies the start and end dates for each term in the 'dd/mm/yyyy' format.

## Code Details

The application processes the data using the following steps:
- Defines a class (`NSWTermDates`) to handle downloading and processing of the CSV data.
- The `NSWTermDates.download_data` method performs a `GET` request to the provided URL and reads the response in a variable (`raw_data`).
- `raw_data` is then split into rows. Each row is checked for its prefix "SCHOOL_TERM" which denotes a new term's start and end dates for a particular state.
- Uses Python's built-in `datetime` library to convert string dates (in the form of 'dd/mm/yyyy') to datetime objects.
- Each term's data is stored in a dictionary (`data_dict`) for that year.
- These term dates are then printed neatly through the `NSWTermDates.print_data` method, which shows the dictionary in a JSON-like format.

## Disclaimer

This project simply presents the data as available from the source and assumes its correctness. Any discrepancies between the represented information and actual dates are likely due to the data source and not the processing performed by this application.

## Dependencies

The following Python packages are required by the script:
- `requests` for performing HTTP requests.
- `datetime` for parsing and working with dates.
- `defaultdict` for efficient dictionary handling.
- `json` for formatting the printed output.

Before running the script, make sure that these libraries are installed and up to date.
## Example Output

The application output is a structured JSON-like dictionary which includes details about the term dates for each year. Here is an example:

```json
{
    "2019": {
        "NSW": {
            "Term 1": {
                "start": "29/01/2019",
                "end": "12/04/2019"
            },
            "Term 2": {
                "start": "29/04/2019",
                "end": "05/07/2019"
            },
            "Term 3": {
                "start": "22/07/2019",
                "end": "27/09/2019"
            },
            "Term 4": {
                "start": "14/10/2019",
                "end": "20/12/2019"
            }
        },
        ...
    },
    "2020": {
        "NSW": {
            "Term 1": {
                "start": "28/01/2020",
                "end": "09/04/2020"
            },
            "Term 2": {
                "start": "27/04/2020",
                "end": "03/07/2020"
            },
            "Term 3": {
                "start": "20/07/2020",
                "end": "25/09/2020"
            },
            "Term 4": {
                "start": "12/10/2020",
                "end": "18/12/2020"
            }
        },
        ...
    },
    ...
}
```