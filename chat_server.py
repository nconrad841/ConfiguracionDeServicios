from concurrent.futures import thread
import socket
import random
from random import randint
from time import sleep
import dhcppython
import tkinter as tk
from tkinter import messagebox
import threading

from test_server_gui_effiongcharles import accept_clients

server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []

def start_server():
    global HOST_ADDR, HOST_PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    thread._start_new_thread(accept_clients, server)

def accept_clients(server):
    while True:
        