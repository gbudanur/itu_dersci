import json
import os


def search(abbreviation, search_type, keyword, check_no_capacity=False):
    matches = []

    folder_path = "course_data"

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"course_data_{abbreviation}.json")

    with open(file_path, "r", encoding="utf-8") as jsonfile:
        course_data = json.load(jsonfile)

    for course in course_data:
        if search_type == "CRN" and course.get("CRN") == keyword:
            if not check_no_capacity or (
                check_no_capacity and course.get("No Capacity") == "No"
            ):
                matches.append(course)
        elif search_type == "Course Code" and course.get("Course Code") == keyword:
            if not check_no_capacity or (
                check_no_capacity and course.get("No Capacity") == "No"
            ):
                matches.append(course)

    return matches


# How to use the search function
# abbreviation = "AKM"
#search_type = "Course Code"
#keyword = "AKM 204"

#results = search(abbreviation, search_type, keyword)

#if results:
#    for course in results:
#       print(f"CRN: {course['CRN']}")
#       print(f"Course Code: {course['Course Code']}")
#       print(f"Course Title: {course['Course Title']}")
#       print(f"No Capacity: {course['No Capacity']}")


#else:
#   print("No matching courses found.")
