import socket
# https://wiki.python.org/moin/UdpCommunication
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hola"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "mensaje:",MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

f=open ("server.png", "rb")
buf = 1024
data = f.read(buf)
while (data):
    if(sock.sendto(data,(UDP_IP,UDP_PORT))):
        print "sending ..."
        data = f.read(buf)