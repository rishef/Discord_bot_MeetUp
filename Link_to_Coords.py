import re


def extract_lat_lon_from_google_maps_url(google_maps_url):
    # Regular expression pattern to extract latitude and longitude from the Google Maps URL
    regex_pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+),\d+z'
    match = re.search(regex_pattern, google_maps_url)
    
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return lat, lon
    else:
        return None, None

# Example usage
google_maps_url = "https://www.google.com/maps/place/Vega+City+Mall/@12.9073525,77.5985446,17z/data=!3m2!4b1!5s0x3bae151b9bec46cd:0xf76bdd18d74e5f8d!4m6!3m5!1s0x3bae157b02ec5755:0xfb70e303df865955!8m2!3d12.9073473!4d77.6011195!16s%2Fg%2F11pv97bj09?entry=ttu"

latitude, longitude = extract_lat_lon_from_google_maps_url(google_maps_url)

print(f'Latitude: {latitude}, Longitude: {longitude}')