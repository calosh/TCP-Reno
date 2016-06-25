import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

buf = 1024
f = open("op.png",'wb')

data , addr = sock.recvfrom(buf)
while True:
    print "mensaje recibido", data
    f.write(data)
    data, addr = sock.recvfrom(buf)
