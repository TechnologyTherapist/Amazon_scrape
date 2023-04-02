import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the website to be scraped
url = 'https://www.relianceretail.com/contactus.html'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content of the website
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the store location divs on the website
store_divs = soup.find_all('div', class_='store-location')

# Create a list to store the extracted data
store_data = []

# Loop through each store location div and extract the relevant data
for store_div in store_divs:
    # Extract the store name and address
    store_name = store_div.find('div', class_='store-title').text.strip()
    store_address = store_div.find('div', class_='store-address').text.strip()

    # Extract the store timings, if available
    store_timings = ''
    timings_div = store_div.find('div', class_='store-timing')
    if timings_div is not None:
        store_timings = timings_div.text.strip()

    # Extract the store coordinates, if available
    store_coords = ''
    map_div = store_div.find('div', class_='map')
    if map_div is not None:
        store_coords = map_div['data-map'].split(',')

    # Extract the store phone number, if available
    store_phone = ''
    phone_div = store_div.find('div', class_='store-phone')
    if phone_div is not None:
        store_phone = phone_div.text.strip()

    # Add the extracted data to the store_data list
    store_data.append({
        'Store Name': store_name,
        'Address': store_address,
        'Timings': store_timings,
        'Latitude': store_coords[0] if store_coords else '',
        'Longitude': store_coords[1] if store_coords else '',
        'Phone Number': store_phone
    })

# Save the store_data list to a CSV file
with open('reliance_stores.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Store Name', 'Address', 'Timings', 'Latitude', 'Longitude', 'Phone Number']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for store in store_data:
        writer.writerow(store)
