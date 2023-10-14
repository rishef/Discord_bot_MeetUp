import requests

def get_places_by_category(lat, lon, category):
    # Replace 'YOUR_API_KEY' with your actual TomTom API key
    api_key = 'YOUR_KEY_HERE'
    base_url = 'https://api.tomtom.com/search/2/categorySearch/'
    url=base_url+category+".json"
    print(url)
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lon,
        #'categorySet': category,
        'limit': 10  # You can adjust the limit as per your requirement
    }

    try:
        response = requests.get(url,params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Parse the JSON response
        data = response.json()

        # Check if the response contains the expected data format
        if 'results' in data and isinstance(data['results'], list):
            places = []
            for result in data['results']:
                if 'poi' in result and 'name' in result['poi'] and 'address' in result:
                    place_name = result['poi']['name']
                    address = result['address']['freeformAddress']
                    places.append({'name': place_name, 'address': address})

            return places
        else:
            return None  # Return None for invalid responses

    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Request Exception: {err}"

# Example usage
lat = 12.937465  # Latitude of the location
lon = 77.5791413  # Longitude of the location
category = 'theatre'  # Replace with the desired category
places = get_places_by_category(lat, lon, category)

#print(type(places))
#print(places)

#Check if places is a valid response before iterating
if places is not None:
    for place in places:
        if isinstance(place, dict) and 'name' in place and 'address' in place:
            print(f"Name: {place['name']}, Address: {place['address']}")
        else:
            print("Error: Invalid data format in the API response.")
else:
    print("Error: Invalid response from the API.")

