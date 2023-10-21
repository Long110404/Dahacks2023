import csv
from pdfminer.high_level import extract_text
import re

# Function to load course names from CSV
def load_course_names_from_csv(class_names):
    course_names = set()
    with open(class_names, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course_names.add(row['Course'].strip())  # Adjusted column name here
    return course_names


# Load course names from CSV
valid_course_names = load_course_names_from_csv('class_names.csv')  # Use the correct filename

# Text from the PDF (for demonstration purposes; this should be replaced by extract_text in real usage)
text = extract_text("DataScience.pdf")

# Remove special characters from the text
text = text.replace('​', '').replace('', '')

# Using regex to identify courses and their articulation status
pattern = r"([A-Z/]+(?:\s+)?[\dCH]+[A-Z]*H?)\s*-\s*[^\n]+(\(\d+\.\d+\))?"

matches = re.findall(pattern, text)

# Set to store course names present in the CSV file
course_names_in_csv = set()

for idx, match in enumerate(matches):
    course_name = match[0].strip()
    course_description = match[1].strip()
    
    # Exclude honors class and classes not present in the CSV
    if "HONORS" in course_description or course_name not in valid_course_names:
        continue
    
    course_names_in_csv.add(course_name)

# Printing the course names present in the CSV file
for course_name in sorted(course_names_in_csv):
    print(course_name)
