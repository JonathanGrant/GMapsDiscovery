import requests
import json
import time
from pathlib import Path
import os


def query_places(zip_code, keyword, api_key):
    places = []
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}+in+{1}&key={2}".format(keyword, zip_code, api_key)
    
    while True:
        response = requests.get(url)
        data = json.loads(response.text)
        places.extend([p for p in data['results'] if zip_code in p['formatted_address']])

        if 'next_page_token' not in data:
            break
        
        time.sleep(2)
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={0}&key={1}".format(data['next_page_token'], api_key)
    
    return places

def update_file(places, filename):
    if not os.path.exists(filename):
        Path(filename).touch()

    with open(filename, 'r') as f:
        existing_places = f.read().splitlines()

    with open(filename, 'a') as f:
        for place in places:
            name = place['name']
            address = place['formatted_address']
            zip_code = address.split(' ')[-2]
            place_data = f"{name}, {address}, {zip_code}"
            if place_data not in existing_places:
                f.write(place_data + '\n')
                print("New place added: ", place_data)

def run(zip_code, keyword):
    api_key = os.environ["GMAPS_API"]

    places = query_places(zip_code, keyword, api_key)
    update_file(places, f'{zip_code}_{keyword}.txt')

for zip in ["10001", "10014", "10002", "10024"]:
    for kw in ["cafe", "climbing", "restaurant", "vegan"]:
        run(zip, kw)
