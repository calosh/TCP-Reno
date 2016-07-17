import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def guardar_info(data):
	fd = open(os.path.join(BASE_DIR,'reno/texto.txt'), 'a')
	fd.write(data)
	fd.close()


