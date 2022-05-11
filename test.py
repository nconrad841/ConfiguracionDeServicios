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