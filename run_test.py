import os
from threading import Thread
import time
import socket
import struct
import binascii

TCP = True
client_num = 3
clients = []
test = 'seguridad' # segirudad, usability

 
def start_server():
    if TCP:
        os.system(f'python3 .\chat_server.py --TCP')
    else:
        os.system(f'python3 .\chat_server.py --UDP')

def start_client():
    if TCP:
        os.system(f'python3 .\chat_client.py --TCP --RUN-TEST')
    else:
        os.system(f'python3 .\chat_client.py --UDP --RUN-TEST')

#start server
server = Thread(target=start_server)
server.start()
time.sleep(0.5)
print('Starting server for testing')
if TCP:
    print('Starting with TCP')
else:
    print('Starting with UDP')

match test:
    case 'velocidad':
        pass
    case 'seguridad':
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(0x0800))
        while True:
            packet = s.recvfrom(1024)
            ethernet_header = packet[0][0:14]
            eth_header = struct.unpack("!6s6s2s", ethernet_header)
            print ("Destination MAC:" + binascii.hexlify(eth_header[0]) + " Source MAC:" + binascii.hexlify(eth_header[1]) + " Type:" + binascii.hexlify(eth_header[2]))
            ipheader = packet[0][14:34]
            ip_header = struct.unpack("!12s4s4s", ipheader)
            print ("Source IP:" + socket.inet_ntoa(ip_header[1]) + " Destination IP:" + socket.inet_ntoa(ip_header[2]))
    case _:
        pass
for i in range(0, client_num):
    print(f'Starting {i} client')
    client = Thread(target=start_client)
    client.start()
    clients.append(client)
