import re
import csv


class Csv:
    """
    Class that represents a csv file
    """

    def __init__(self, filename, target_path, headers):
        """
        Args:
            filename (string): Name of the csv file
            target_path (string): Wher save the file
            headers (list): Which header for the file
        """
        self.filename = filename
        self.target_path = target_path
        self.headers = headers
        self.path = None

    def create_csv_file(self):
        """Create the file"""
        with open(
            f"{self.target_path}/{self.filename}.csv", "w", newline="", encoding="utf-8"
        ) as fi:
            writer = csv.writer(fi, delimiter=";")
            writer.writerow(self.headers)
        self.path = f"{self.target_path}/{self.filename}.csv"
        fi.close

    def append_into_csv(self, data):
        """Append the data into current file

        Args:
            data (list): Wich data to append
        """
        with open(self.path, "a") as fi:
            writer = csv.writer(fi, delimiter=";")
            writer.writerow(
                [re.sub("[^A-Za-z0-9,\/.-_'\" -]", "", str(d)) for d in data]
            )
        fi.close
