from concurrent.futures import thread
import socket
import random
from random import randint
import time
import datetime
import threading

server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

clients = []
clients_names = []
max_clients = 5

def start_server():
    print(f'Starting Server...')
    global HOST_ADDR, HOST_PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for UDP: socket.SOCK_DGRAM
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(max_clients)  # server is listening for client connection

    #threading._start_new_thread(accept_clients, (server, ''))
    accept_clients(server, '')

def accept_clients(server, not_needed):
    global max_clients
    print(f'Accepting max. {max_clients} Clients: ')
    while True:
        client, addr = server.accept()

        #send_receive_client_message(client, addr)
        threading._start_new_thread(send_receive_client_message, (client, addr))
        

def send_receive_client_message(client_connected, client_ip_addr):
    global server, clients, clients_names
    client_name = ''
    client_name = client_connected.recv(4096).decode()
    print(f'Server:\t\'{client_name}\' knocks at the door..')

    if client_name in clients_names:
        msg = f'Server:\t\'{client_name}\' invalid, already in list, chose an other one'
        print(msg)

        client_connected.send(msg.encode())
        send_receive_client_message(client_connected, client_ip_addr)

    # client accepted
    else:
        msg = f'Server:\tConnection successfull with \'{client_name}\''
        print(msg)
        client_connected.send(msg.encode())

        clients.append(client_connected)
        clients_names.append(client_name)

        inform_clients_about_others(client_connected)

        while True:
            if client_connected.fileno() == -1:
                print(f'Server:\tConnection closed with {client_name}')
                clients_names.remove(client_name)
                clients.remove(client_connected)
                break
            try:
                data = client_connected.recv(4096).decode()
            except ConnectionResetError:
                print(f'Server:\tConnection closed with {client_name} -> ConnectionResetError')
                client_connected.close()
                clients_names.remove(client_name)
                clients.remove(client_connected)
                break

            if not data: break
            if data == 'exit': break
            if data == 'info': 
                inform_clients_about_others(client_connected)
                continue

            msg = f'\'{client_name}\':\t{data}'
            print(msg)
            
            # send message to all
            for client in clients:
                client.send(msg.encode())


def inform_clients_about_others(client_connected):
    global clients_names, clients
    if len(clients) != len(clients_names):
        print('something went wrong')
        exit()
    if len(clients) != 0: 
        msg = 'Chatmembers are: '
        for name in (clients_names):
            msg += f'\'{name}\', '
        client_connected.send(msg.encode())
        



if __name__ == '__main__':
    start_server() 