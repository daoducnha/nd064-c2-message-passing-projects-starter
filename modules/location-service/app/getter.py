import grpc
import locations_pb2
import locations_pb2_grpc

print("Getting location by id...")

channel = grpc.insecure_channel("localhost:5005")
stub = locations_pb2_grpc.LocationServiceStub(channel)

response = stub.GetById(locations_pb2.LocationById(location_id="1"))
print(response)