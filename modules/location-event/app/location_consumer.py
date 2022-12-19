from kafka import KafkaConsumer
import json
from services import LocationService

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'localhost:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
for message in consumer:
    location = json.loads(message.value.decode('utf-8'))
    LocationService.create(location)

