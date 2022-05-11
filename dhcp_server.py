import socket
import dhcppython
import ipaddress
import struct
import random

MAX_BYTES = 1024

serverPort = 67
clientPort = 68

class DHCP_server(object):

    def server(self):
        print("DHCP server is starting...\n")
        
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        s.bind(('', serverPort))
        dest = ('255.255.255.255', clientPort)

        while 1:
            try:
                print("Wait DHCP discovery.")
                data, address = s.recvfrom(MAX_BYTES)
                print("Receive DHCP discovery.")
                pkt_disc = dhcppython.packet.DHCPPacket.from_bytes(data)
                MAC = pkt_disc.chaddr
                xid = pkt_disc.xid
                print(f'MAC is: {MAC}, ID = {xid}')
        
                print("Send DHCP offer.")
                ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                print(f'Suggested IP is {ip}')
                data = dhcppython.packet.DHCPPacket.Offer(MAC, seconds=0, tx_id=xid,\
                    yiaddr=ipaddress.IPv4Address(ip))
                data = data.asbytes
                s.sendto(data, dest)
                while 1:
                    try:
                        print("Wait DHCP request.")
                        data, address = s.recvfrom(MAX_BYTES)
                        pkt_req = dhcppython.packet.DHCPPacket.from_bytes(data)
                        print("Receive DHCP request.")
                        #print(data)

                        print("Send DHCP pack.\n")
                        data = dhcppython.packet.DHCPPacket.Ack(\
                            MAC, seconds=0, tx_id=xid, yiaddr=ipaddress.IPv4Address(ip))
                        data = data.asbytes
                        s.sendto(data, dest)
                        break
                    except:
                        raise
            except:
                raise


if __name__ == '__main__':
    dhcp_server = DHCP_server()
    dhcp_server.server()