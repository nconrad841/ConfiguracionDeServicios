import socket
import random
from random import randint
from time import sleep
import dhcppython
import tkinter as tk
from tkinter import messagebox
import threading

HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

entName = "Testname"

def connect():
    global username, client
    if len(entName < 1):
        print("Name should be longer than 1")
    else:
        username = entName
        global HOST_PORT, HOST_ADDR
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(username.encode())

