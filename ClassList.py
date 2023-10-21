import requests
from bs4 import BeautifulSoup
import pandas as pd

# Request the website content
url = "https://www.deanza.edu/schedule/gen-ed-classes.html"  # Replace this with the actual URL if different
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Locate the table with the class listings (you might need to adjust this depending on the actual structure)
table = soup.find_all("table")[0]  # Assuming it's the first table

rows = table.find_all('tr')
header = [th.text for th in rows[0].find_all('th')]
data = []

for row in rows[1:]:  # Skip the header row
    data.append([td.text for td in row.find_all('td')])

# Convert data into a DataFrame and then to CSV
df = pd.DataFrame(data, columns=header)
df.to_csv('gen_ed_class_listings.csv', index=False)
