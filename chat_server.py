from concurrent.futures import thread
import socket
import random
from random import randint
from time import sleep
import dhcppython
import tkinter as tk
from tkinter import messagebox
import threading


server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

clients = []
clients_names = []
max_clients = 5

def start_server():
    print(f'Starting Server, max clients: {max_clients}')
    global HOST_ADDR, HOST_PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for UDP: socket.SOCK_DGRAM
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(max_clients)  # server is listening for client connection

    #threading._start_new_thread(accept_clients, (server, ''))
    accept_clients(server, '')

def accept_clients(server, not_needed):
    print('Starting Accepting Clients')
    while True:
        client, addr = server.accept()

        #send_receive_client_message(client, addr)
        threading._start_new_thread(send_receive_client_message, (client, addr))
        

def send_receive_client_message(client_connected, client_ip_addr):
    global server, clients, clients_names
    client_name = ''
    client_name = client_connected.recv(4096).decode()
    print(f'Server:\n\'{client_name}\' knocks at the door..')

    if client_name in clients_names:
        msg = f'Server:\n\'{client_name}\' invalid, already in list, chose an other one'
        print(msg)

        client_connected.send(msg.encode())
        send_receive_client_message(client_connected, client_ip_addr)

    else:
        clients.append(client_connected)
        clients_names.append(client_name)

        msg = f'Server:\nConnection successfull with \'{client_name}\''
        print(msg)
        client_connected.send(msg.encode())

        while True:
            if client_connected.fileno() == -1:
                clients_names.remove(client_name)

            data = client_connected.recv(4096).decode()
            if not data: break
            if data == 'exit': break

            print(data)




start_server()