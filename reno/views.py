from django.http import HttpResponse
from django.shortcuts import render

import socket
# https://wiki.python.org/moin/UdpCommunication
import sys
import os
from time import sleep
import matplotlib.pyplot as plt
from metodos import *
from PIL import Image

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    return render(request, 'index.html')

def sender_image(request):
    if request.method == 'POST':
        if request.FILES:
            file = request.FILES['imagen']
            # http://stackoverflow.com/questions/3111779/how-can-i-get-the-file-name-from-request-files
            # print file.name           # Gives name
            # print file.content_type   # Gives Content type text/html etc
            # print file.size           # Gives file's size in byte
            UDP_IP = "127.0.0.1"
            UDP_PORT = 5005

            print "UDP target IP:", UDP_IP
            print "UDP target port:", UDP_PORT

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Se elimina el archivo en donde se guardan los datos para el grafico
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            os.remove(os.path.join(BASE_DIR, 'reno/texto.txt'))
            #f = open("reset.png", "rb")
            buf = 512

            cont = 1
            estado = 0
            contC = 1

            umbral = 4096  # 512*8
            VC = 512  # 1MSS
            congestion = 6144  # 512*12
            aux_congestion = congestion
            # lista = []
            data = True
            while (data):
                data = file.read(VC)
                if not data:
                    break
                if estado == 0:
                    print "Arranque lento", VC / 512
                    if VC < umbral:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        cont += 1
                        VC *= 2
                    elif VC >= umbral:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        VC += 512
                        cont += 1
                        estado = 1
                        continue
                    else:
                        print 'error'
                elif estado == 1:
                    print "Evitacion de la congestion", VC / 512
                    if VC < congestion:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        VC += 512
                        cont += 1
                    elif VC >= congestion:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        umbral = VC / 2
                        VC = umbral
                        cont += 1
                        estado = 2
                        # congestion = (random.randint((umbral + 512) / 512, (aux_congestion - 512) / 512)) * 512
                        continue
                    else:
                        print "Errror case 1"

                elif estado == 2 and contC <= 2:
                    print "Recuperacion Rapida", VC / 512
                    if VC < congestion:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        VC += 512
                        cont += 1
                    elif VC >= congestion and contC < 2:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        umbral = VC / 2
                        VC = umbral
                        estado = 2
                        contC += 1
                        cont += 1

                        # congestion = (random.randint((umbral + 512) / 512, (aux_congestion - 512) / 512)) * 512

                        continue
                    elif VC >= congestion and contC == 2:
                        sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
                        # Recibe ACK
                        recv_data, addr = sock.recvfrom(2048)
                        print "Datos Recibidos: ", recv_data
                        guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
                        umbral = 4096
                        VC = 512
                        estado = 0
                        cont += 1
                        contC = 1
                        # congestion = (random.randint((umbral+512) / 512, (aux_congestion-512) / 512)) * 512
                        print "Congestion ", congestion
                        print "Umbral ", umbral
                        continue
                    else:
                        print "Error case 2"

                sleep(1)

            sock.sendto(" " + "<->" + 'fin', (UDP_IP, UDP_PORT))
            sock.close()

    return render(request, 'sender.html')

def receiver_image(request):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    # buf = 1024
    buf = 16384

    f = open(os.path.join(BASE_DIR,'static/miImagen.png'), 'wb')

    data, addr = sock.recvfrom(buf)
    # Envia ACK
    sock.sendto("ACK", addr)
    cont = ""
    info = []

    while True:
        print "PACKAGE RECEIVED..."
        info = data.split("<->")
        # print info
        print info[1]
        if info[1] == 'fin':
            break
        # f.write(data)
        f.write(info[0])
        # buf=buf*2
        data, addr = sock.recvfrom(buf)
        # Envia ACK
        sock.sendto("ACK", addr)


    #response = HttpResponse(mimetype="image/png")
    #f.save(response, "PNG")
    #return response
    return render(request, 'receiver.html')