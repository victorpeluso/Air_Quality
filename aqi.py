import main_functions
import requests
import folium

"""TASK 6"""
def get_api_key(filename):
    # Gather data from the JSON file
    data = main_functions.read_from_file(filename)
    # Return the API key as a string from the dictionary
    return data['aqi_api_key']

my_aqi_api_key = get_api_key("api_key.json")

print(my_aqi_api_key)

"""TASK 7"""
def get_aqi_data(api_key):
    url = "http://api.airvisual.com/v2/nearest_city?key="
    url_aqi = url + api_key

    # Make the API request
    response = requests.get(url_aqi)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the result into a JSON file
        main_functions.save_to_file(response.json(), "aqi.json")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")

get_aqi_data(my_aqi_api_key)

"""TASK 8"""
def generate_map(data_filename,zoom_start):
    aqi_data = main_functions.read_from_file(data_filename)
    lat = aqi_data['data']['location']['coordinates'][1]
    long = aqi_data['data']['location']['coordinates'][0]
    m = folium.Map(location=[lat, long], zoom_start=zoom_start)
    folium.Marker(
        location=[lat, long],
        popup='AQI Station',
        icon=folium.Icon()
    ).add_to(m)
    m.save("map.html")

generate_map("aqi.json", 10)

"""TASK 9"""
def display_aqi_info(data_filename):
    aqi_data = main_functions.read_from_file(data_filename)
    tempC = aqi_data['data']['current']['weather']['tp']
    tempF = (tempC * 9/5) + 32
    humid = aqi_data['data']['current']['weather']['hu']
    aqius = aqi_data['data']['current']['pollution']['aqius']

    if aqius <= 50:
        air_quality = "good"
    elif 51 <= aqius <= 100:
        air_quality = "moderate"
    elif 101 <= aqius <= 150:
        air_quality = "unhealthy for sensitive groups"
    elif 151 <= aqius <= 200:
        air_quality = "unhealthy"
    elif 201 <= aqius <= 300:
        air_quality = "very unhealthy"
    else:
        air_quality = "hazardous"

    print(f"The temperature is {tempC}ºC or {tempF:.1f}ºF, the humidity is {humid}%, "
          f"and the index shows that the air quality is {air_quality}.")

display_aqi_info("aqi.json")