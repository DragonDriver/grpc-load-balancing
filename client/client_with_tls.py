from __future__ import print_function
import logging
import time
import datetime
import random
import os

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

endpoint = '127.0.0.1:58243'
endpoint = '192.168.99.101:31323'
endpoint = '192.168.99.101:443'
endpoint = 'greeter.demo.com:443'
endpoint = 'greeter.demo.com:50051'

print(f"endpoint: {endpoint}")

MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 1024 * 1024 * 1024))

options=[
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
]

with open('../k8s/tls.crt', 'rb') as f:
    trusted_certs = f.read()

credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

def run():
    num = 3
    length = 512 * 1
    #print(f"test num: {num}")
    #print(f"length of workload: {length}")
    workload = [random.random() for _ in range(length)]

    #print(f"[{datetime.datetime.now()}] low overhead request begin")
    begin = time.time()
    # with grpc.secure_channel(endpoint, credentials, options=options) as channel:
    with grpc.insecure_channel(endpoint) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        for _ in range(num):
            response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            print(response)
    end = time.time()
    #print(f"[{datetime.datetime.now()}] low overhead request end")
    #print(f"time cost: {(end - begin)}")

    #print(f"[{datetime.datetime.now()}] high overhead request begin")
    #begin = time.time()
    #with grpc.secure_channel(endpoint, credentials, options=options) as channel:
    #    stub = helloworld_pb2_grpc.GreeterStub(channel)
    #    for _ in range(num):
    #        response = stub.SayGoodBye(helloworld_pb2.HighOverheadRequest(req=workload))
    #end = time.time()
    #print(f"[{datetime.datetime.now()}] high overhead request end")
    #print(f"time cost: {(end - begin)}")

if __name__ == '__main__':
    logging.basicConfig()
    run()
