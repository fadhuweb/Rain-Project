import requests
import json
import datetime
import logging

# Configure logging
logging.basicConfig(filename='skyscanner_data_collection.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Function to save JSON data to a file
def save_data(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Data saved to {filename}")

# Function to handle API requests
def make_request(url, headers, params=None, payload=None, request_type="GET"):
    try:
        if request_type == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif request_type == "POST":
            response = requests.post(url, headers=headers, json=payload)
        
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error collecting data from {url}: {e}")
        return None

# Function to collect data from various Skyscanner APIs
def collect_skyscanner_data():
    # Headers for Skyscanner API
    headers = {
        "x-rapidapi-key": "7b8e8854a0msh6554f0a24d22801p1d770cjsn8edfbd963cf5",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    # 1. Collect airport data
    url_airports = "https://sky-scanner3.p.rapidapi.com/flights/airports"
    airports_data = make_request(url_airports, headers)
    if airports_data:
        save_data(f'skyscanner_airports_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json', airports_data)
    
    # 2. Collect roundtrip flight data
    url_roundtrip = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
    params_roundtrip = {"fromEntityId": "PARI"}
    roundtrip_data = make_request(url_roundtrip, headers, params=params_roundtrip)
    if roundtrip_data:
        save_data(f'skyscanner_roundtrip_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json', roundtrip_data)

    # 3. Collect flight detail data
    url_detail = "https://sky-scanner3.p.rapidapi.com/flights/detail"
    params_detail = {"token": "eyJhIjoxLCJjIjowLCJpIjowLCJjYyI6ImVjb25vbXkiLCJvIjoiWU1RQSIsImQiOiJZSFoiLCJkMSI6IjIwMjQtMDctMDgifQ==", "itineraryId": "18395-2407081425--31147-0-18169-2407081705"}
    detail_data = make_request(url_detail, headers, params=params_detail)
    if detail_data:
        save_data(f'skyscanner_detail_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json', detail_data)

    # 4. Collect "search-everywhere" data
    url_everywhere = "https://sky-scanner3.p.rapidapi.com/flights/search-everywhere"
    params_everywhere = {"fromEntityId": "NYCA", "type": "oneway"}
    everywhere_data = make_request(url_everywhere, headers, params=params_everywhere)
    if everywhere_data:
        save_data(f'skyscanner_everywhere_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json', everywhere_data)

if __name__ == "__main__":
    collect_skyscanner_data()
