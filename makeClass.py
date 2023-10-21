import csv

# File names
main_file = 'class_names.csv'
other_file = 'gen_ed_class_listings.csv'

# Header
header = "Course"

# Step 1: Read the main CSV
with open(main_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    main_courses = {row[0].strip() for row in reader}

# Step 2: Read the "Course" column from the other CSV
with open(other_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    new_courses = {row[0].strip() for row in reader}

# Step 3: Merge the two sets
merged_courses = main_courses.union(new_courses)

# Step 4: Write the merged set back into the main CSV
with open(main_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([header])  # header
    for course in sorted(merged_courses):
        writer.writerow([course])
