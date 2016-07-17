import socket
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#buf = 1024
buf = 16384

f = open("image2.png",'wb')

data , addr = sock.recvfrom(buf)
sock.sendto("Response 1", addr)
cont = ""
info = []

while True:
    print "PACKAGE RECEIVED..."
    info = data.split("<->")
    #print info
    print info[1]
    if info[1]=='fin':
        break
    #f.write(data)
    f.write(info[0])
    #buf=buf*2
    data, addr = sock.recvfrom(buf)
    sock.sendto("Response 1", addr)


    #time.sleep(0.5)