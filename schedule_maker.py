import csv
from pdfminer.high_level import extract_text
import re

# Function to load course names and their titles from CSV
def load_course_names_from_csv(class_names):
    course_names = set()
    course_titles = {}  # Dictionary to store course titles
    with open(class_names, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course = row['Course'].strip()
            course_names.add(course)
            course_titles[course] = row['Title'].strip()  # Store the course title
    return course_names, course_titles

# Load course names and their titles from CSV
valid_course_names, course_titles = load_course_names_from_csv('class_names.csv')

# Text from the PDF
text = extract_text("ComputerScience.pdf")

# Remove special characters from the text
text = text.replace('​', '').replace('', '')

# Using regex to identify courses and their articulation status
pattern = r"([A-Z/]+(?:\s+)?[\dCH]+[A-Z]*H?)\s*-\s*([^\n]+?)(\(\d+\.\d+\))?(\n|$)"

matches = re.findall(pattern, text)

# Dictionary to store course information
course_info = {}

for match in matches:
    course_name = match[0].strip()
    course_description = match[1].strip()
    course_units = match[2] if match[2] else ''

    # Exclude courses that end with "H" (honors courses)
    if course_name[-1] == "H":
        continue

    # Only include the course if it's in the CSV
    if course_name in valid_course_names:
        course_info[course_name] = {
            "description": course_description,
            "units": course_units
        }
        # Check for prerequisites based on trailing letters
        if course_name[-1].isalpha():
            base_course = course_name[:-1]
            # Loop through letters in reverse order starting from the identified course's letter
            for letter in reversed(range(ord('A'), ord(course_name[-1]))):
                potential_prerequisite = f"{base_course}{chr(letter)}"
                if potential_prerequisite in valid_course_names and potential_prerequisite not in course_info:
                    # If the course is not in the text, use the title from the CSV and units from the identified course
                    course_info[potential_prerequisite] = {
                        "description": course_titles[potential_prerequisite], 
                        "units": course_info[course_name]['units']
                    }

# Printing the course names present in the CSV file along with their descriptions and units
print("CLASS NEEDED:")
for idx, (course_name, info) in enumerate(sorted(course_info.items())):
    print(f"{idx + 1}. {course_name} - {info['description']} {info['units']}")
