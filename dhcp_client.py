import socket
import threading
import random
import secrets
import binascii
from random import randint
from scrapy.all import get_if_raw_hwaddr, conf
from time import sleep
import sys
import struct
xid = randint(0, 0xFFFFFFFF)
mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))

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
        data = DHCP_client.discover_get();
        s.sendto(data, dest)
        
        data, address = s.recvfrom(MAX_BYTES)
        print("Receive DHCP offer.")
        self.data = data
        self.transID = bytes([0x39, 0x03, 0xF3, 0x26])
        self.offerIP = ''
        self.nextServerIP = ''
        self.DHCPServerIdentifier = ''
        self.leaseTime = ''
        self.router = ''
        self.subnetMask = ''
        self.DNS = []
        self.unpack()
        self.printOffer()
        #print(data)

        print("Send DHCP request.")
        data = DHCP_client.request_get();
        s.sendto(data, dest)
        
        data,address = s.recvfrom(MAX_BYTES)
        print("Receive DHCP pack.\n")
        #print(data)

    def discover_get():
        OP = bytes([0x01]) #Message type: Boot Request (1)
        HTYPE = bytes([0x01]) #Hardware type: Ethernet
        HLEN = bytes([0x06]) #Hardware address length: 6
        HOPS = bytes([0x00]) #Hops: 0
        XID = bytes([0x39, 0x03, 0xF3, 0x26]) # #Transaction ID: should be random
        SECS = bytes([0x00, 0x00]) #Seconds elapsed: 0
        FLAGS = bytes([0x00, 0x00]) #Bootp flags: 0x8000 (Broadcast) + reserved flags
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00]) #Client IP address: 0.0.0.0
        YIADDR = bytes([0x00, 0x00, 0x00, 0x00]) #Your (client) IP address: 0.0.0.0
        SIADDR = bytes([0x00, 0x00, 0x00, 0x00]) #Server IP address: 0.0.0.0
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00]) #Gateway IP address: 0.0.0.0
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00]) 
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
        Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCPOptions1 = bytes([53 , 1 , 1])
        DHCPOptions2 = bytes([50 , 4 , 0xC0, 0xA8, 0x01, 0x64])


        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2

        return package

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

    def printOffer(self):
        data = self.data
        key = ['DHCP Server', 'Offered IP address', 'subnet mask', 'lease time (s)' , 'default gateway']
        val = [self.DHCPServerIdentifier, self.offerIP, self.subnetMask, self.leaseTime, self.router]
        for i in range(4):
            print('{0:20s} : {1:15s}'.format(key[i], val[i]))
        
        print('{0:20s}'.format('DNS Servers') + ' : ', end='')
        if self.DNS:
            print('{0:15s}'.format(self.DNS[0]))
        if len(self.DNS) > 1:
            for i in range(1, len(self.DNS)): 
                print('{0:22s} {1:15s}'.format(' ', self.DNS[i])) 
	

    def unpack(self):
        if self.data[4:8] == self.transID :
            data = self.data
            self.offerIP = '.'.join(map(lambda x:str(x), data[16:20]))
            self.nextServerIP = '.'.join(map(lambda x:str(x), data[20:24]))  #c'est une option
            self.DHCPServerIdentifier = '.'.join(map(lambda x:str(x), data[245:249]))
            self.leaseTime = str(struct.unpack('!L', data[251:255])[0])
            self.router = '.'.join(map(lambda x:str(x), data[257:261]))
            self.subnetMask = '.'.join(map(lambda x:str(x), data[263:267]))
            #dnsNB = int(data[268]/4)
            #for i in range(0, 4 * dnsNB, 4):
            #    self.DNS.append('.'.join(map(lambda x:str(x), data[269 + i :269 + i + 4])))
    
                

if __name__ == '__main__':
    dhcp_client = DHCP_client()
    dhcp_client.client()