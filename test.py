import json

with open("brainlox_courses.json", "r") as f:
    course_data = json.load(f)

print(f"Total courses: {len(course_data)}")
