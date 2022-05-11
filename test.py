mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))



class DHCPDiscover:
    def __init__(self, xid, hw):
        self.TransactionID = struct.pack('IL', xid)
        self.macInBytes = hw

    def DHCP(self):
        packet = b''
        Op = b'\x01'   #Message type: Boot Request (1)
        HwType = b'\x01'   #Hardware type: Ethernet
        HwAddrLen = b'\x06'   #Hardware address length: 6
        HopC = b'\x00'   #Hops: 0 
        TransactionID = self.transactionID       #Transaction ID
        NumOfSec = b'\x00\x00'    #Seconds elapsed: 0
        Flags_B_Res = b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
        ciaddr = b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
        yiaddr = b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
        siaddr = b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
        giaddr = b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
        #packet = b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
        chwaddr = self.macInBytes
        chwpadding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
        srcHostname = b'\x00' * 67  #Server host name not given
        bootFilename = b'\x00' * 125 #Boot file name not given
        magic_cookie = b'\x63\x82\x53\x63'   #Magic cookie: DHCP
        msg_type= b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
        #packet = b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
        clientID = b'\x3d\x06' + selfmacInBytes
        par_req_list = b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
        end = b'\xff'   #End Option
        
        packet = Op + HwType + HwAddrLen + HopC + TransactionID + NumOfSec + Flags_B_Res + ciaddr + yiaddr + siaddr + giaddr + chwaddr\
            chwpadding + srcHostname + bootFilename + magic_cookie + msg_type + clientID + par_req_list + end
        
        return packet

discover_get

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


Offer
        OP = bytes([0x02])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        YIADDR = bytes([0xC0, 0xA8, 0x01, 0x64]) #192.168.1.100
        SIADDR = bytes([0xC0, 0xA8, 0x01, 0x01]) #192.168.1.1
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00])
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
        Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCPOptions1 = bytes([53 , 1 , 2]) # DHCP Offer
        DHCPOptions2 = bytes([1 , 4 , 0xFF, 0xFF, 0xFF, 0x00]) #255.255.255.0 subnet mask
        DHCPOptions3 = bytes([3 , 4 , 0xC0, 0xA8, 0x01, 0x01]) #192.168.1.1 router
        DHCPOptions4 = bytes([51 , 4 , 0x00, 0x01, 0x51, 0x80]) #86400s(1 day) IP address lease time
        DHCPOptions5 = bytes([54 , 4 , 0xC0, 0xA8, 0x01, 0x01]) # DHCP server
        
        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2 + DHCPOptions3 + DHCPOptions4 + DHCPOptions5

        return package