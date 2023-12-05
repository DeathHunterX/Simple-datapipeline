import os
import time
from kafka import KafkaProducer
import configparser
import requests
import json
import random

# IQAir API endpoint
iqair_api_url = "http://api.airvisual.com/v2/"

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 30))

config = configparser.ConfigParser()
config.read('iqairmap_service.cfg')
api_credential = config['iqairmap_api_credential']
access_token = api_credential['access_token']


def flatten_and_modify_json(json_obj, parent_key='', sep='_'):
    """
    Recursively flatten a nested JSON structure into a single-layer dictionary.
    Combines 'current_pollution_ts' and 'current_weather_ts' into 'current_ts'.
    Separates the 'coordinates' attribute into 'latitude' and 'longitude' if present.
    Removes 'location_type' attribute.

    Parameters:
    - json_obj: The input JSON object.
    - parent_key: Internal parameter for recursion (do not specify).
    - sep: Separator for combining keys (default is '_').

    Returns:
    - A flattened and modified dictionary.
    """
    items = []
    for key, value in json_obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if key == 'location' and isinstance(value, dict) and 'coordinates' in value:
            items.extend([(f"{parent_key}latitude", value['coordinates'][0]), (f"{parent_key}longitude", value['coordinates'][1])])
        elif key == 'current' and isinstance(value, dict):
            pollution_ts = value['pollution']['ts'] if 'pollution' in value and 'ts' in value['pollution'] else None
            weather_ts = value['weather']['ts'] if 'weather' in value and 'ts' in value['weather'] else None

            if pollution_ts and weather_ts and pollution_ts == weather_ts:
                items.append((f"{new_key}_ts", pollution_ts))
                del value['pollution']['ts']
                del value['weather']['ts']
            else:
                if pollution_ts:
                    items.append((f"{new_key}_pollution_ts", pollution_ts))
                    del value['pollution']['ts']
                if weather_ts:
                    items.append((f"{new_key}_weather_ts", weather_ts))
                    del value['weather']['ts']

            items.extend(flatten_and_modify_json(value, new_key, sep=sep).items())
        elif key != 'location_type' and isinstance(value, dict):
            items.extend(flatten_and_modify_json(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)

# Get random state function
# Random getting 1 state for going next step is get data in random city
def get_random_state(api_key, country):
    base_url = f"{iqair_api_url}states?country={country}&key={api_key}"

    response = requests.get(base_url)

    if response.status_code == 200:
        states = [state["state"] for state in response.json()["data"]]
        return random.choice(states)
    else:
        print(f"Error getting states: {response.status_code}")
        return None

# Get random city function
# Random getting 1 city for going next step is get data in specific city and state
def get_random_city(api_key, state, country):
    base_url = f"{iqair_api_url}cities?state={state}&country={country}&key={api_key}"

    response = requests.get(base_url)

    if response.status_code == 200:
        cities = [city["city"] for city in response.json()["data"]]
        return random.choice(cities)
    else:
        print(f"Error getting cities in {state}: {response.status_code}")
        return None

def get_air_quality(api_key, city, state, country):
    base_url = f"{iqair_api_url}city?city={city}&state={state}&country={country}&key={api_key}"

    response = requests.get(base_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting air quality data. Status code: {response.status_code}, Response content: {response.content}")
        return None

# Get IQAir data
def get_IQAir_data(country):
    # air_quality_data = {}

    # Get a random state
    random_state = get_random_state(access_token, country)

    if random_state is not None:
        # Get a random city within the selected state
        random_city = get_random_city(access_token, random_state, country)

        if random_city is not None:
            # Fetch air quality data for the randomly selected city and state
            air_quality_data = get_air_quality(access_token, random_city, random_state, country)
            
            if air_quality_data is not None:
                # Modify data after fetched
                modified_air_quality_data = flatten_and_modify_json(air_quality_data["data"])
                return modified_air_quality_data
            
    return {}

def run():
    country = "USA"

    iterator = 0
    print("Setting up IQAir producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    while True:
        
        # adding prints for debugging in logs
        print("Sending new IQAir report iteration - {}".format(iterator))
        addresses_data = get_IQAir_data(country)
        print(addresses_data)
        producer.send(TOPIC_NAME, value=addresses_data)
        print("New IQAir data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()
