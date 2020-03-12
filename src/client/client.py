import socket
import time
import sys

SEND_PORT = 50001

MAX_SUPPORTED_SERVERS = 254

class NetCacheClient:

    def __init__(self, n_servers=1):
        self.n_servers = n_servers
        self.servers = []

        self.port = SEND_PORT

        self.udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_servers_ips()

        # store all latencies of the requests sent (used for evaluation)
        self.latencies = []


    # the IP addresses assigned to servers are based on the assignment
    # strategy defined at the p4app.json file; the basic l2 strategy
    # that we are using assigns IP addresses starting from 10.0.0.1
    # and assigns incrementing addresses to defined hosts
    def get_servers_ips(self):
        if self.n_servers > MAX_SUPPORTED_SERVERS:
            print("Error: Exceeded maximum supported servers")
            sys.exit()

        for i in range(self.n_servers):
            self.servers.append("10.0.0." + str(i+1))

    def get_node(self, key):
        return self.servers[(key % self.n_servers)]

    def udp(self, key, seq=0, suppress=False):
        start_time = time.time()

        self.udps.connect((self.get_node(key), self.port))
        self.udps.send(str.encode("client1"))

        data = self.udps.recv(1024)
        
        latency = time.time() - start_time
        self.latencies.append(latency)

        if not suppress:
            print(data)

    def tcp(self, key, seq = 0, suppress=False):
        tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcps.connect((self.get_node(key), self.port))

        start_time = time.time()

        tcps.send(str.encode("client1"))
        status = tcps.recv(1024)

        latency = time.time() - start_time
        self.latencies.append(latency)
        
        if not suppress:
            print(status)

        tcps.close()

def main(n_servers, suppress):
    client = NetCacheClient(n_servers=n_servers)
    total_start = time.time()

    k = 0
    while True:
        time.sleep(0.1)
        # client.tcp(k, suppress=suppress)
        client.udp(k, suppress=suppress)
        
        k += 1
                
        spend_time = time.time() - total_start

    print(spend_time)


if __name__=="__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--n-servers', help='number of servers', type=int, required=False, default=1)
    parser.add_argument('--suppress', help='suppress output', action='store_true')
    args = parser.parse_args()
    
    main(args.n_servers, args.suppress)
