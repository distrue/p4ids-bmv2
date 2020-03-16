from collections import deque

import socket
import logging
import threading
import sys
import os

STATISTICS_REFRESH_INTERVAL = 30.0

SERVER_PORT = 50001


class KVServer:

    def __init__(self, host, suppress=False, max_listen=10):
        # simple in-memory key value store, represented by a dictionary
        self.kv_store = {}

        # server ip address
        self.host = host
        # server name
        self.name = 'server' + self.host.split('.')[-1]

        self.port = SERVER_PORT

        # suppress printing messages
        self.suppress = suppress
        # udp server socket
        self.udpss = None
        #tcp server socket
        self.tcpss = None
        # max clients to listen to
        self.max_listen = max_listen
        
        self.blocking = False
        # queue to store incoming requests while blocking
        self.incoming_requests = deque()

        # keep number of requests dispatched to use for evaluation
        self.requests_cnt = 0

    def activate(self):

        # enable logging for debuggin purposes
        logging.basicConfig(
                filename='log/{}.log'.format(self.name),
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.DEBUG,
                datefmt='%d-%m-%Y %H:%M:%S')

        # create udp socket server
        self.udpss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpss.bind((self.host, self.port))

        # create tcp socket server
        self.tcpss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpss.bind((self.host, self.port))
        self.tcpss.listen(1)

        # spawn new thread that serves incoming udp (read) queries
        server_udp_t = threading.Thread(target=self.handle_client_udp_request)
        server_udp_t.start()

        # spawn new thread that serves incoming tcp (put/delete) queries
        server_tcp_t = threading.Thread(target=self.handle_client_tcp_request)
        server_tcp_t.start()

        # self.periodic_request_report()

    def periodic_request_report(self):
        t = threading.Timer(STATISTICS_REFRESH_INTERVAL, self.periodic_request_report)
        t.daemon = True
        t.start()

        if not self.suppress:
            print('[{}] Number of requests received = {}'.format(self.name, self.requests_cnt))


    def handle_client_udp_request(self):
        while True:
            if not self.blocking and len(self.incoming_requests) > 0:
                packet, addr = self.incoming_requests.popleft()

            else:
                packet, addr = self.udpss.recvfrom(1024)
                print(packet)
            
            if self.blocking:
                self.incoming_requests.append((packet, addr))
                continue
            
            else:
                msg = "UDP"
                self.udpss.sendto(msg, addr)
            
            print("udp request")


    # serves incoming tcp queries (i.e. put/delete)
    def handle_client_tcp_request(self):
        while True:
            conn, addr = self.tcpss.accept()
            packet = conn.recv(1024)

            msg = "TCP"
            conn.sendall(msg)
            conn.close()

            print("tcp request")


def main(suppress_output):

    from subprocess import check_output

    # dynamically get the IP address of the server
    server_ip = check_output(['hostname', '--all-ip-addresses']).decode('utf-8').rstrip()
    server = KVServer(server_ip, suppress=suppress_output)

    server.activate()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--suppress-output', help='supress output printing messages', action='store_true')
    args = parser.parse_args()

    main(args.suppress_output)
