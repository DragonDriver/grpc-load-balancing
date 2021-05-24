from __future__ import print_function
import logging
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    with grpc.insecure_channel('127.0.0.1:51920') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        num = 50
        for _ in range(num):
            time.sleep(2)
            response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
