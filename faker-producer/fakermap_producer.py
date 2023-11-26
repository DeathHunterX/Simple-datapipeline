import os
import time
from kafka import KafkaProducer
from decimal import Decimal
from faker import Faker
import json

fake = Faker()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")


def get_addresses_data():
    return {
        "id": fake.uuid4(),
        "street": fake.street_address(),
        "streetName": fake.street_name(),
        "buildingNumber": fake.building_number(),
        "city": fake.city(),
        "zipcode": fake.postcode(),
        "country": fake.country(),
        "country_code": fake.country_code(),
        "latitude": fake.latitude(),
        "longitude": fake.longitude(),
    }

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x, default=decimal_serializer).encode("utf-8"),
    )

    while True:
        
        # adding prints for debugging in logs
        print("Sending new Faker report iteration - {}".format(iterator))
        addresses_data = get_addresses_data()
        print(addresses_data)
        producer.send(TOPIC_NAME, value=addresses_data)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()
