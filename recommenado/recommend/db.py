import csv
from typing import Tuple, TextIO

def read_db() -> Tuple[TextIO, csv.reader]:
    """
    Reads the article database and returns a reader object with the data

    TODO: Consider using https://github.com/asg017/sqlite-vec to provide a lightweight vector extension
    for sqllite in a run-anywhere environment
    """
    csvfile = open('./recommenado/recommend/articlesembeds.csv', newline='')
    articlereader = csv.reader(csvfile, delimiter=';')
    return csvfile, articlereader