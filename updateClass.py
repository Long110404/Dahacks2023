import csv

# File names
main_file = 'class_names.csv'
listing_file = 'clean_class_listings.csv'

# Read the main CSV into a dictionary
course_dict = {}
with open(main_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for row in reader:
        course = row[0].strip()
        course_dict[course] = {'Course': course}

# Read the clean_class_listings.csv and update the course_dict
with open(listing_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for row in reader:
        course = row[1].strip()
        title = row[4].replace('"', '').strip()  # Remove quotation marks from the title
        if course in course_dict:
            course_dict[course]['Title'] = title

# Write the updated dictionary back into the main CSV
with open(main_file, 'w', newline='') as f:
    fieldnames = ['Course', 'Title']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # header
    for _, course_details in course_dict.items():
        writer.writerow(course_details)
