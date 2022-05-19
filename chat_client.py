import socket
import random
from random import randint
from time import sleep
import dhcppython
import tkinter as tk
from tkinter import messagebox
import threading
import time

HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
client = None

username = "Testname"

def connect():
    global client

    # connect to server
    global HOST_PORT, HOST_ADDR, client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))

    manage_username(client)

    threading._start_new_thread(receive_message_from_server, (client, "m"))
    #receive_message_from_server(client)

def manage_username(client):
    global username
    while True:
        username = input("Enter username : ")
        if len(username) < 1:
            print("Name should be longer than 1")
        else:
            client.send(username.encode())
            resp = client.recv(4096).decode()
            if 'Connection successfull' in resp:
                print(f'Username \'{username}\' accepted by the server')                
                break
            else:
                print(f'Username already in usage, choose new name')


def receive_message_from_server(client_connected, not_used):
    while True:
        #connection still available
        if client_connected.fileno() != -1:
            msg_from_server = client_connected.recv(4096).decode()
            if msg_from_server:
                print(f'{msg_from_server}')
        else:
            exit()
        

def send_message_to_server(msg):
    global client
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        exit()    



# welcome message
commands = f'You have the following options:\n\t'
commands += f'\'info\' for getting info about other users\n\t'
commands += f'\'-> <USERNAME>: \' for sending a message to only one member\n\t'
commands += f'\'exit\' for closing the connection'
print(commands)
#msg = input("Enter name : ")

connect()
while True:
    msg = input('Enter your message: ')
    if msg == 'exit':
        exit()
    send_message_to_server(msg)
