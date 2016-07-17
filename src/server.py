import socket
# https://wiki.python.org/moin/UdpCommunication
import sys
import os
from time import sleep
import matplotlib.pyplot as plt
from metodos import *
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Se elimina el archivo en donde se guardan los datos para el grafico
os.remove('texto.txt')
f=open ("reset.png", "rb")
print type(f)
print sys.getsizeof(f)
buf = 512

cont = 1
estado = 0
contC = 1

umbral=4096 #512*8
VC=512 # 1MSS
congestion=6144 #512*12
aux_congestion = congestion
#lista = []
data = True
while (data):
	data = f.read(VC)
	if not data:
		break
	if estado==0:
		print "Arranque lento",VC/512
		if VC<umbral:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ",recv_data
			guardar_info(str(cont)+','+str(VC / 512)+'\n')
			cont += 1
			VC*=2
		elif VC>=umbral:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ", recv_data
			guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
			VC += 512
			cont += 1
			estado=1
			continue
		else:
			print 'error'
	elif estado==1:
		print "Evitacion de la congestion", VC/512
		if VC<congestion:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ", recv_data
			guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
			VC += 512
			cont += 1
		elif VC>=congestion:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ", recv_data
			guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
			umbral=VC/2
			VC=umbral
			cont += 1
			estado=2
			#congestion = (random.randint((umbral + 512) / 512, (aux_congestion - 512) / 512)) * 512
			continue
		else:
			print "Errror case 1"

	elif estado==2 and contC<=2:
		print "Recuperacion Rapida", VC / 512
		if VC < congestion:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ", recv_data
			guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
			VC += 512
			cont += 1
		elif VC >= congestion and contC<2:
			sock.sendto(data + "<->" + str(cont), (UDP_IP, UDP_PORT))
			# Recibe ACK
			recv_data, addr = sock.recvfrom(2048)
			print "Datos Recibidos: ", recv_data
			guardar_info(str(cont) + ',' + str(VC / 512) + '\n')
			umbral = VC / 2
			VC = umbral
			estado = 2
			contC+=1
			cont += 1

			#congestion = (random.randint((umbral + 512) / 512, (aux_congestion - 512) / 512)) * 512

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
			#congestion = (random.randint((umbral+512) / 512, (aux_congestion-512) / 512)) * 512
			print "Congestion ", congestion
			print "Umbral ", umbral
			continue
		else:
			print "Error case 2"

	sleep(1)

sock.sendto(" " + "<->" + 'fin', (UDP_IP, UDP_PORT))
sock.close()
