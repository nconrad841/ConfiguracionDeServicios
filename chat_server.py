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
client_names = []
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
        accept_clients_UDP(server)

def RecvData_UDP(server, recvPackets):
    while True:
        try:
            data, addr = server.recvfrom(1024)
        except ConnectionResetError:
            print('Some host disconnected {addr}, {data}')
            continue
        recvPackets.put((data,addr))

def accept_clients_UDP(server):
    global clients, client_names

    recvPackets = queue.Queue()
    threading.Thread(target=RecvData_UDP,args=(server,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data, addr = recvPackets.get()
            data = data.decode('utf-8')
            
            #new client -> 1. message is username
            if (addr not in clients):
                client_name = data
                # username already in use
                if client_name in client_names:
                    msg = f'Server -> \'{client_name}\' invalid, already in list, chose an other one'
                    server.sendto(msg.encode(), addr)
                    continue
                
                # username accepted
                clients.append(addr)                
                client_names.append(client_name)
                msg = f'Server -> Connection successfull with \'{client_name}\''
                server.sendto(msg.encode(), addr)
                
                #inform_clients_about_others() # TODO: Check that
                continue
                

            if data == '{info}': 
                #inform_clients_about_others()
                continue
        
            # send message to all
            # in clients are the adresses stored
            msg = f'{data}'
            #print(msg)
            for client in clients:     
                if client == addr:
                    #print(f'Data should not be sent to: {client_names[clients.index(addr)]}')
                    continue
                server.sendto(msg.encode(), client)

def accept_clients_TCP(server):
    global max_clients
    print(f'Accepting max. {max_clients} Clients: ')
    while True:
        client, addr = server.accept()
        threading._start_new_thread(receive_send_client_message_TCP, (client, addr))
        
def receive_send_client_message_TCP(client_connected, client_ip_addr):
    global server, clients, client_names
    client_name = ''
    client_name = client_connected.recv(4096).decode()
    print(f'Server -> \'{client_name}\' knocks at the door..')

    if client_name in client_names:
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
        client_names.append(client_name)

        inform_clients_about_others()

        while True:
            try:
                data = client_connected.recv(4096).decode()
            except ConnectionResetError:
                print(f'Server -> Connection closed with \'{client_name}\' -> ConnectionResetError')
                client_connected.close()
                client_names.remove(client_name)
                clients.remove(client_connected)
                break
            
            if (not data) or (data == '{quit}') or (client_connected.fileno() == -1):
                print(f'Server -> Connection closed with \'{client_name}\'')
                client_connected.close()
                client_names.remove(client_name)
                clients.remove(client_connected)
                break
                
            if data == '{info}': 
                inform_clients_about_others()
                continue

            msg = f'{data}'
            print(msg)
            
            # send message to all
            for client in clients:
                if client is client_connected:
                    continue
                client.send(msg.encode())



def inform_clients_about_others():
    global client_names, clients
    if len(clients) != len(client_names):
        print('something went wrong')
        exit()
    if len(clients) != 0: 
        msg = 'Server -> Chatmembers are now: '
        names = ' '.join(client_names).replace(' ', ', ')
        msg += names

        for name, client in zip(client_names, clients):
            
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
    