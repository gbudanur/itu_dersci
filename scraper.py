import requests
from lxml import html
import json
import time
import os


def scraper(course_abbreviation):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    url = f"https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS&derskodu={course_abbreviation}"

    response = requests.get(url)

    if response.status_code == 200:
        page_content = html.fromstring(response.content.decode("windows-1254"))

        course_table = page_content.xpath("/html/body/div[1]/div[2]/div/div[3]/table")[
            0
        ]

        course_data = []

        for row in course_table.xpath(".//tr")[1:]:
            columns = row.xpath(".//td")

            course_code_element = columns[1].find(".//a")
            course_code = (
                course_code_element.text_content().strip()
                if course_code_element is not None
                else ""
            )

            capacity = columns[9].text_content().strip()
            enrolled = columns[10].text_content().strip()

            no_capacity = "Yes" if capacity == enrolled else "No"

            course_info = {
                "CRN": columns[0].text_content().strip(),
                "Course Code": course_code,
                "Course Title": columns[2].text_content().strip(),
                "Teaching Method": columns[3].text_content().strip(),
                "Instructor": columns[4].text_content().strip(),
                "Building": columns[5].text_content().strip(),
                "Day": columns[6].text_content().strip(),
                "Time": columns[7].text_content().strip(),
                "Room": columns[8].text_content().strip(),
                "Capacity": capacity,
                "Enrolled": enrolled,
                "Reservation": columns[11].text_content().strip(),
                "Major Restriction": columns[12].text_content().strip(),
                "Prerequisites": columns[13].text_content().strip(),
                "Class Restrictions": columns[14].text_content().strip(),
                "No Capacity": no_capacity,
            }

            course_data.append(course_info)

        if course_data and course_data[0]["CRN"] == "CRN":
            course_data.pop(0)

        last_update = time.strftime("%H:%M:%S %d.%m.%Y")
        course_data.append({"Last Update": last_update})

        folder_path = "course_data"

        os.makedirs(folder_path, exist_ok=True)

        filename = os.path.join(folder_path, f"course_data_{course_abbreviation}.json")

        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(course_data, jsonfile, indent=4, ensure_ascii=False)

        print(f"Course data saved to {filename}")

    else:
        print(
            f"Failed to retrieve data for course abbreviation {course_abbreviation}. Status code: {response.status_code}"
        )


if __name__ == "__main__":
    course_abbreviation = input("Enter course abbreviation: ")
    scraper(course_abbreviation)
