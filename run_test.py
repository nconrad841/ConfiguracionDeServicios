import os
from threading import Thread
import time

TCP = False
client_num = 5
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
print('starting server for testing')


for i in range(0, client_num):
    client = Thread(target=start_client)
    client.start()
    clients.append(client)
