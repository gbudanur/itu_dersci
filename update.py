from scraper import scraper
import json
from time import sleep
import random as rand


def update():
    with open("course_abbreviations.json", "r") as jsonfile:
        course_abbreviations = json.load(jsonfile)

    for course_abbreviation in course_abbreviations:
        delay = rand.randint(1, 3) / 10
        sleep(delay)
        scraper(course_abbreviation)


if __name__ == "__main__":
    update()
