from concurrent import futures
import logging
import socket
import os
import signal

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

with open('../k8s/tls.key', 'rb') as f:
    private_key = f.read()
with open('../k8s/tls.crt', 'rb') as f:
    certificate_chain = f.read()

def get_local_ip():
    if os.getenv("IP"):
        return os.getenv("IP")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

DEFAULT_PORT = 50051

def get_port():
    return os.getenv("PORT", DEFAULT_PORT)

LOCAL_IP = get_local_ip()
PORT = get_port()

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!, I am {LOCAL_IP}:{PORT}")

    def SayGoodBye(self, request, context):
        return helloworld_pb2.HighOverheadResponse(res=request.req)

MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 1024 * 1024 * 1024))

def serve():
    server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=10),
                options=[
                    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                ],
            )
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    server.add_secure_port(f'[::]:{PORT}', server_credentials)
    server.start()
    #try:
    #    while True:
    #        signal.pause()
    #except KeyboardInterrupt:
    #    pass
    #server.stop(0)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

