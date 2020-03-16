import socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.bind(('10.0.0.1', 50001))
data, addr = sock.recvfrom( 200 )
print(data.decode(), addr[0], addr[1])
