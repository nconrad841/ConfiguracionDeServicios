from ast import Is
from concurrent.futures import thread
import socket
import random
from random import randint
import time
import datetime
import threading
import time
import argparse
import queue

server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
IS_TCP = True

clients = []
clients_names = []
max_clients = 5

def start_server():
    print(f'Starting Server...')
    global HOST_ADDR, HOST_PORT
    if IS_TCP:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for UDP: socket.SOCK_DGRAM
        server.bind((HOST_ADDR, HOST_PORT))
        server.listen(max_clients)  # server is listening for client connection
        accept_clients_TCP(server)
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((HOST_ADDR, HOST_PORT))
        data, addr = server.recvfrom(1024)

def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    clients = set()
    recvPackets = queue.Queue()
    threading.Thread(target=RecvData,args=(server,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    server.sendto(data.encode('utf-8'),c)
    

def accept_clients_TCP(server):
    global max_clients
    print(f'Accepting max. {max_clients} Clients: ')
    while True:
        client, addr = server.accept()
        threading._start_new_thread(receive_send_client_message_TCP, (client, addr))
        

def receive_send_client_message_TCP(client_connected, client_ip_addr):
    global server, clients, clients_names
    client_name = ''
    client_name = client_connected.recv(4096).decode()
    print(f'Server -> \'{client_name}\' knocks at the door..')

    if client_name in clients_names:
        msg = f'Server -> \'{client_name}\' invalid, already in list, chose an other one'
        print(msg)

        client_connected.send(msg.encode())
        receive_send_client_message_TCP(client_connected, client_ip_addr)

    # client accepted
    else:
        msg = f'Server -> Connection successfull with \'{client_name}\''
        print(msg)
        client_connected.send(msg.encode())

        clients.append(client_connected)
        clients_names.append(client_name)

        inform_clients_about_others()

        while True:
            try:
                data = client_connected.recv(4096).decode()
            except ConnectionResetError:
                print(f'Server -> Connection closed with \'{client_name}\' -> ConnectionResetError')
                client_connected.close()
                clients_names.remove(client_name)
                clients.remove(client_connected)
                break
            
            if (not data) or (data == '\{quit\}') or (client_connected.fileno() == -1):
                print(f'Server -> Connection closed with \'{client_name}\'')
                client_connected.close()
                clients_names.remove(client_name)
                clients.remove(client_connected)
                break
                
            if data == '{info}': 
                inform_clients_about_others()
                continue

            msg = f'{data}'
            #print(msg)
            
            # send message to all
            for client in clients:
                if client is client_connected:
                    continue
                client.send(msg.encode())



def inform_clients_about_others():
    global clients_names, clients
    if len(clients) != len(clients_names):
        print('something went wrong')
        exit()
    if len(clients) != 0: 
        msg = 'Server -> Chatmembers are now: '
        names = ' '.join(clients_names).replace(' ', ', ')
        msg += names

        for name, client in zip(clients_names, clients):
            
            client.send(msg.encode())
        



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--TCP", '-T', help="Use TCP", default=False, action="store_true")
    parser.add_argument("--UDP", '-U', help="Use UDP", default=False, action="store_true")
    args = parser.parse_args()

    if args.TCP == args.UDP:
        print('Something went wrong, set one flag --TCP or --UDP')
        exit()
    if args.TCP:
        print('Service starting TCP')
    elif args.UDP:
        print('Service starting UDP')
        IS_TCP = False

    start_server() 
    