import socket
import threading
import random
import secrets
import binascii
from random import randint
from time import sleep
import sys
import struct
import dhcppython
import ipaddress

xid = randint(0, 0xFFFFFFFF)
mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

MAX_BYTES = 1024

serverPort = 67
clientPort = 68

class DHCP_client(object):
    def client(self):
        print("DHCP client is starting...\n")
        dest = ('<broadcast>', serverPort)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('0.0.0.0', clientPort))

        print("Send DHCP discovery.")
        chaddr= "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))        
        data = dhcppython.packet.DHCPPacket.Discover(chaddr)
        xid = data.xid
        print(f'MAC is: {chaddr}, ID = {xid}')
        data=data.asbytes
        s.sendto(data, dest)
        
        print("Receive DHCP offer.")
        data, address = s.recvfrom(MAX_BYTES)
        pkt = dhcppython.packet.DHCPPacket.from_bytes(data)
        print(f'Suggested IP is: {pkt.yiaddr}')
    

        print("Send DHCP request.")
        data = dhcppython.packet.DHCPPacket.Request(\
            chaddr, seconds=0, tx_id=xid).asbytes
        s.sendto(data, dest)
        
        data,address = s.recvfrom(MAX_BYTES)
        print("Receive DHCP ack.\n")
        #print(data)

    def request_get():
        OP = bytes([0x01])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        YIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        SIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x0C, 0x29, 0xDD]) 
        CHADDR2 = bytes([0x5C, 0xA7, 0x00, 0x00])
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
        Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCPOptions1 = bytes([53 , 1 , 3])
        DHCPOptions2 = bytes([50 , 4 , 0xC0, 0xA8, 0x01, 0x64])
        DHCPOptions3 = bytes([54 , 4 , 0xC0, 0xA8, 0x01, 0x01])
	
        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2 +  DHCPOptions3

        return package
                

if __name__ == '__main__':
    dhcp_client = DHCP_client()
    dhcp_client.client()