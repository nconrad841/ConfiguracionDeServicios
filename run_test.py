import os
from threading import Thread
import time

TCP = False
client_num = 2
clients = []

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


for i in range(0, client_num):
    print(f'Starting {i} client')
    client = Thread(target=start_client)
    client.start()
    clients.append(client)
