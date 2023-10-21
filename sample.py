from pdfminer.high_level import extract_text
import re

# Text from the PDF (for demonstration purposes; this should be replaced by extract_text in real usage)
text = extract_text("DataScience.pdf")

# Remove special characters from the text
text = text.replace('​', '').replace('', '')

# Using regex to identify courses and their articulation status
pattern = r"([A-Z/]+\s*[\dCH]+[A-Z]*H?)\s*-?\s*([^\n]+)(\(\d+\.\d+\))?"

matches = re.findall(pattern, text)

# Dictionary to store mapping between UC and CC classes
uc_to_cc_mapping = {}

for idx, match in enumerate(matches):
    course_name = match[0].strip()
    course_description = match[1].strip()
    course_units = match[2] if match[2] else ""
    full_course = f"{course_name} - {course_description} {course_units}".strip()

    # Exclude honors class for now
    if "HONORS" in course_description:
        continue
    
    subsequent_index = text.find(full_course) + len(full_course)
    subsequent_text = text[subsequent_index:subsequent_index + 200].split("\n")[0].strip()

    # Check if the course is from UC or CC
    if "No Course Articulated" in subsequent_text:
        uc_to_cc_mapping[full_course] = "No course articulated"
    elif "←" in subsequent_text:
        subsequent_text = subsequent_text.split("←")[1].strip()
        courses = re.findall(pattern, subsequent_text)
        if courses:
            uc_to_cc_mapping[full_course] = ' and '.join([f"{c[0]} - {c[1]} {c[2]}" for c in courses])
        else:
            uc_to_cc_mapping[full_course] = "Not Specified"
    else:
        uc_to_cc_mapping[full_course] = "Not Specified"

# Formatting the list
formatted_list = []
for idx, (uc_course, cc_courses) in enumerate(uc_to_cc_mapping.items(), 1):
    formatted_list.append(f"{idx}. {uc_course} = {cc_courses}")

# Printing the formatted list
for item in formatted_list:
    print(item)
