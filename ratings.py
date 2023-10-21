from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_professor_rating(professor_name):
    # Setting up Chrome options to bypass SSL checks
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Set up the Selenium browser instance with the above options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the main page
    driver.get('https://www.ratemyprofessors.com')

    # Wait for the elements to load
    time.sleep(3)  # You can adjust this delay
    
    # Close the cookie notice pop-up
    try:
        close_button = driver.find_element(By.XPATH, "//button[text()='Close']")
        close_button.click()
    except Exception as e:
        print(f"Failed to close the pop-up: {e}")

    # Input the school name "De Anza"
    school_input = driver.find_element(By.XPATH, "//input[@placeholder='Your school']")
    school_input.send_keys("De Anza")
    time.sleep(2)  # Allow dropdown results to appear
    school_input.send_keys(Keys.RETURN)

    # Wait for the page to load after selecting the school
    time.sleep(3)

    # Input the professor's name
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Professor name']")
    search_box.send_keys(professor_name)
    search_box.send_keys(Keys.RETURN)

    # At this point, the website will have loaded the results page.
    # Extract the relevant information from the results (this step requires further inspection of the result page's structure)
    # For example:
    # rating = driver.find_element(By.CLASS_NAME, 'RatingValue__Numerator-qw8sqy-2 gxuTRq').text

    # Clean up and close the browser instance
    driver.quit()

    # Return the rating (or modify to return other relevant data)
    # return f"Rating for {professor_name}: {rating}/5"

# Example usage:
prof_name = "Sukhjit Singh"
print(get_professor_rating(prof_name))
