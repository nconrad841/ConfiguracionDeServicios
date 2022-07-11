from socket import AF_INET, socket, SOCK_STREAM
import random
from random import randint
from time import sleep
from tkinter import *
from tkinter import font
from tkinter import ttk
from threading import Thread
import time
import argparse
import os

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8080
BUFSIZ = 4096

IS_TCP = True
RUN_TEST = False

client = None
username = ""

def receive_message_from_server():
    global client, username
    while True:
        #connection still available
        if client.fileno() == -1:
            print(f'Client -> Connection closed with Server')
            break
        try:
            msg_from_server = client.recv(BUFSIZ).decode()
            if msg_from_server == (f'Server -> \'{username}\' invalid, already in list, chose an other one'):
                msg_list.insert(END, 'Username already in use, choose other username')
                username = ''
                continue
            elif 'Server -> Connection successfull with' in msg_from_server:
                username = msg_from_server[39:-1]
                top.title(f"Client {username}")
                continue
            print(msg_from_server)
            msg_list.insert(END, msg_from_server)

        except ConnectionResetError:
             print(f'Client:\tConnection closed with Server -> ConnectionResetError')
             break
        

def send_message_to_server(event=None):
    global client, username

    msg = my_msg.get()
    my_msg.set("")  # Clears input field.

    if username == '':
        username = msg

    # send message
    client.send(msg.encode())
    msg_list.insert(END, f'{username} -> {msg}')

    if msg == "{quit}":
        client.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send_message_to_server()


parser = argparse.ArgumentParser()
parser.add_argument("--username", '-u', help="Username", default="")
parser.add_argument("--TCP", '-T', help="Use TCP", default=False, action="store_true")
parser.add_argument("--UDP", '-U', help="Use UDP", default=False, action="store_true")
parser.add_argument("--RUN-TEST", '-R', help="Run a test for velocidad, usabilidad, seguridad", default=False, action="store_true")
args = parser.parse_args()
username = args.username


#start GUI
#############################################
top = Tk()
top.title(f"Client {username}")

txt_frame = Frame(top)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("")

scrollbar = Scrollbar(txt_frame)
msg_list = Listbox(txt_frame, height=15, width=150, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
txt_frame.pack()

# welcome message
commands = f'You have the following options:'
msg_list.insert(END, commands)
commands = '{info} for getting info about other users'
msg_list.insert(END, commands)
#commands += f'\'-> <USERNAME>: \' for sending a message to only one member\n\t'
commands = '{quit} for closing the connection'
msg_list.insert(END, commands)
if username == "":
    commands = 'Enter your username'
    msg_list.insert(END, commands)
else: print(f'Your username {username}')

entry_frame = Entry(top, textvariable=my_msg)
entry_frame.bind("<Return>", send_message_to_server)
entry_frame.pack()
send_button = Button(top, text="Send", command=send_message_to_server)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
#############################################

if IS_TCP:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for UDP: socket.SOCK_DGRAM
else:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
client.connect((SERVER_ADDR, SERVER_PORT))


if RUN_TEST:
    username = os.urandom(8)

receive_thread = Thread(target=receive_message_from_server)
receive_thread.start()

# send username if existing
if username != '':
    client.send(username.encode())

# for start of GUI  Interface
mainloop()
