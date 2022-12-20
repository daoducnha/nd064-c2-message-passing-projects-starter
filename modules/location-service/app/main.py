import time
from concurrent import futures

import grpc
import locations_pb2
import locations_pb2_grpc
from kafka import KafkaProducer
import json

import logging

logging.basicConfig(filename="locations_log.txt", level=logging.DEBUG)

class LocationService(locations_pb2_grpc.LocationServiceServicer):

    def Getter(self, request, context):
        location_id = request.location_id
        if location_id:
            location = LocationService.retrieve(location_id)
            if location:
                return locations_pb2.LocationResponse(
                    id = location.id,
                    person_id = location.person_id,
                    longitude = location.longitude,
                    latitude = location.latitude,
                    creation_time = location.creation_time,
                )
            else:
                logging.warning("Cannot found location id: %s", location_id) 
        else:
            logging.info("Missing location id in request") 


    def Create(self, request, context):
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time
        }

        print(request_value)

        TOPIC_NAME = "locations"
        TOPIC_SERVER = "localhost:9002"

        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        producer.send(TOPIC_NAME, json.dumps(request_value).encode())
        producer.flush()
        return item_pb2.ItemMessage(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()


try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)