import socket
import random
from random import randint
from time import sleep
import dhcppython

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
                

if __name__ == '__main__':
    dhcp_client = DHCP_client()
    dhcp_client.client()