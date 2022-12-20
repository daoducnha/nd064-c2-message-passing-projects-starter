import grpc
import locations_pb2
import locations_pb2_grpc


print("Sending location payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = locations_pb2_grpc.LocationServiceStub(channel)

location = locations_pb2.LocationMessage(
    person_id="1",
    creation_time="2022-11-11",
    latitude="123456",
    longitude="123456"
)

response = stub.Create(location)