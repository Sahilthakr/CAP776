import requests

def get_coordinates(city, api_key):
    """Fetches latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    geocoding_response = requests.get(geocoding_url)

    if geocoding_response.status_code == 200:
        geocoding_data = geocoding_response.json()
        if geocoding_data:
            latitude = geocoding_data[0]['lat']
            longitude = geocoding_data[0]['lon']
            return latitude, longitude
        else:
            print("City not found in Geocoding API response.")
            return None, None
    else:
        print(f"Error fetching geocoding data. Status Code: {geocoding_response.status_code}")
        return None, None