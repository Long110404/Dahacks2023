import csv

# Function to update class_names.csv with titles from clean_class_listings.csv
def update_class_names_with_titles():
    # File names
    main_file = 'class_names.csv'
    listing_file = 'clean_class_listings.csv'

    # Read the main CSV into a dictionary
    course_dict = {}
    with open(main_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
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

# Function to extract unique course and instructor combinations from gen_ed_class_listings.csv
def extract_unique_courses_and_professors():
    # File paths
    input_file_path = "gen_ed_class_listings.csv"
    output_file_path = "gen_ed_unique_courses_and_professors.csv"

    # Process CSV
    with open(input_file_path, 'r', errors='replace') as infile, open(output_file_path, 'w', newline='') as outfile:
        # Remove NUL bytes and store cleaned content
        cleaned_content = infile.read().replace('\x00', '')
        
        # Use the cleaned content for the CSV reader
        csvreader = csv.reader(cleaned_content.splitlines())
        csvwriter = csv.writer(outfile)
        
        # Write header for the new file
        csvwriter.writerow(['Course', 'Instructor'])
        
        # Skip the header of the input CSV
        header = next(csvreader)
        
        # Get the indices of the necessary columns
        crn_idx = header.index('CRN')
        course_idx = header.index('Course')
        instructor_idx = header.index('Instructor')
        
        seen_combinations = set()  # To track combinations we've already seen
        
        for row in csvreader:
            # Extract necessary columns
            crn = row[crn_idx]
            course = row[course_idx]
            instructor = row[instructor_idx]
            
            # Check if 'CRN' value is a number and if instructor is not empty
            try:
                int(crn)
                if instructor and (course, instructor) not in seen_combinations:  # Ensure instructor name is not empty and combination is unique
                    csvwriter.writerow([course, instructor])
                    seen_combinations.add((course, instructor))  # Mark this combination as seen
            except ValueError:
                # Skip the row if 'CRN' is not a number
                pass

# Execute the functions
update_class_names_with_titles()
extract_unique_courses_and_professors()
