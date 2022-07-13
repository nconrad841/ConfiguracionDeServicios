from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
import random
from random import randint
from time import sleep
from tkinter import *
from tkinter import font
from tkinter import ttk
from threading import Thread
import time
from datetime import datetime
import argparse
import os
from random import choice
from string import ascii_uppercase

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8080
BUFSIZ = 4096

IS_TCP = True
RUN_TEST = False

client = None
username = ""

def receive_message_from_server():
    global client, username, RUN_TEST
    while True:
        #connection still available
        if client.fileno() == -1:
            print(f'Client -> Connection closed with Server')
            break
        try:
            msg_from_server = client.recv(BUFSIZ).decode()
            #print(msg_from_server)

            if msg_from_server == (f'Server -> \'{username}\' invalid, already in list, chose an other one'):
                msg_list.insert(END, 'Username already in use, choose other username')
                username = ''
                continue
            elif ('Server -> Connection successfull with' in msg_from_server) and (username == ''):
                username = msg_from_server[39:-1]

            msg_list.insert(END, msg_from_server)

        except ConnectionResetError:
            print(f'Client -> Connection closed with Server, ConnectionResetError')
            break
        except ConnectionAbortedError:
            print(f'Client -> Connection closed with Server, ConnectionAbortedError')
            break
        

def send_message_to_server(event=None):
    global client, username

    msg = f'{my_msg.get()}'

    if username == '': # user just entered username
        username = my_msg.get()
        if username == '':
            pass
    else:
        msg = f'{username} -> {msg}'

    my_msg.set("")  # Clears input field


    # send message
    client.send(msg.encode())
    msg_list.insert(END, f'{msg}')

    if msg == "{quit}":
        client.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send_message_to_server()

###################################################
# TEST SECTION
def receive_message_for_test():
    global client, username, RUN_TEST
    while True:
        #connection still available
        if client.fileno() == -1:
            print(f'Client -> Connection closed with Server')
            break
        try:
            msg_from_server = client.recv(BUFSIZ).decode()
            if not "Server -> " in msg_from_server:
                if IS_TCP: filenname = username + '_TCP'
                elif IS_TCP: filenname = username + '_UDP'
                with open(f'{filenname}.txt', 'a') as f:
                    f.write(f' --- {msg_from_server}, {str(datetime.now())} --- \n')
            
        except ConnectionResetError:
            print(f'Client:\tConnection closed with Server -> ConnectionResetError')
            break
        except ConnectionAbortedError:
            print(f'Client:\tConnection closed with Server -> ConnectionAbortedError')
            break
    print("Test run aborted")

def run_test():
    global client, username
    if username == '':
        username = ''.join(choice(ascii_uppercase) for i in range(12))
    client.send(username.encode())

    # receiving message 
    receive_thread = Thread(target=receive_message_for_test)
    receive_thread.start()

    i = 0
    while True:
        
        msg = f'{username} -> {i}: {datetime.now()}'
        msg = msg + ', ' + ''.join(choice(ascii_uppercase) for i in range(20000))                

        client.send(msg.encode())
        i += 1
        time.sleep(0.01) # importatn variable for testing speed

###################################################



parser = argparse.ArgumentParser()
parser.add_argument("--username", '-u', help="Username", default="")
parser.add_argument("--TCP", '-T', help="Use TCP", default=False, action="store_true")
parser.add_argument("--UDP", '-U', help="Use UDP", default=False, action="store_true")
parser.add_argument("--RUN-TEST", '-R', help="Run a test for velocidad, usabilidad, seguridad", default=False, action="store_true")
args = parser.parse_args()

username = args.username
IS_TCP = args.TCP
RUN_TEST = args.RUN_TEST

if args.TCP == args.UDP:
    print('Something went wrong, set one flag --TCP or --UDP')
    exit()

if IS_TCP:
    print('Running TCP')
    client = socket(AF_INET, SOCK_STREAM) #for UDP: socket.SOCK_DGRAM
    client.connect((SERVER_ADDR, SERVER_PORT))
else:
    client = socket(AF_INET, SOCK_DGRAM) 
    client.connect((SERVER_ADDR, SERVER_PORT))



if args.RUN_TEST:
    print('Test is now running')
    run_test()
    exit()


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


receive_thread = Thread(target=receive_message_from_server)
receive_thread.start()

# send username if existing
if username != '':
    client.send(username.encode())

# for start of GUI Interface
mainloop()
