import socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.sendto('String'.encode(), ('127.0.0.1', 50001))
