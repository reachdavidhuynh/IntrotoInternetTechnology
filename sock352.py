#David Huynh and Kevan Channer 

import binascii
import socket as syssock
import struct
import sys
import random 
from enum import Enum


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    global sock
    sock=syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    global sendPort
    global receivePort
    sendPort = int(UDPportTx)
    receivePort = int(UDPportRx)
    global randomSeq 
    randomSeq = random.randint(0,100)
    randomSeqStart = randomSeq
    sock.bind(('', int(UDPportRx)))
    global sizeofpkt
    global destination 
    global initflag
    initflag = False 
    global initflag2
    initflag2 = False
    global getpktsize 
    pass
    
class flag(Enum):
    SOCK352_SYN = 1
    SOCK352_FIN = 2
    SOCK352_ACK = 4
    SOCK352_RESET = 8
    SOCK352_HAS_OPT = 16
    SOCK352_DATA = 32

class socket:
    
    def __init__(self):  # fill in your code here 
        return
    
    def bind(self,address):
        return 


     #return 1 if ack, 2 if data, 3 if fin 
    def sock352_get_packet(self, package, recvsize):
        global msgQueue
        global sendport
        global destination
        #msgQueue=Queue()
        sock352PktHdrData = '!BBHQQL' + str(recvsize) + 's' 
        sizeofpkt = sock352PktHdrData
        print sizeofpkt
        version,flag,header_len,sequence_no,ack_no,payload_len,msgbuffer=struct.unpack(sizeofpkt,package)
        print "flag", flag
        if flag == 1 or flag == 2 or flag == 32:         #currentRecv=0
            if flag == 1: 
                print "Type: Ack packet"
                myAddress=(destination, sendPort)
                version=1
                flag=4
                ack_no=sequence_no+1
                sock352PktHdrData = '!BBHQQL'
                udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
                ack_packet = udpPkt_hdr_data.pack(version, flag, header_len, sequence_no, ack_no, payload_len)
                sock.sendto(ack_packet,myAddress)
                return (1, sequence_no)
                #pass
            if flag == 32:
                print "Type: Data packet"
                #msgQueue.put_nowait(msgbuffer)
                myAddress = (destination, sendPort)
                flag=4
                header_len=len(sizeofpkt)
                ack_no=sequence_no+1
                payload_len=0
                #sock352PktHdrData = '!BBHQQL'+str(recvsize)+'b'
                sock352PktHdrData = '!BBHQQL'
                udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
                ack_packet = udpPkt_hdr_data.pack(version, flag, header_len, sequence_no, ack_no, payload_len)
                sock.sendto(ack_packet,myAddress)
                print msgbuffer
                #currentRecv+=len(msgbuffer)
                return msgbuffer
                #pass
                #return (2, sequence_no)
            if flag == 2: 
                print "Type: Fin packet"
                return (3, sequence_no)
            #If no correct type
        else: 
            print "invalid flag" 
            return 0
        return 0 
        #return (0, 0)

    def connect(self,address):  # fill in your code here 
        global sendPort
        global receivePort
        global sizeofpkt
        randomSeq = random.randint(0, 100)
        msgbuffer = "This is a connection request from client"
        sock352PktHdrData = '!BBHQQL' + str(len(msgbuffer)) + 's' 
        print str(len(msgbuffer))
        sizeofpkt = sock352PktHdrData
        udpPkt_hdr_data = struct.Struct(sizeofpkt)
        version = 1
        flags = 1
        header_len = 0
        sequence_no = randomSeq
        ack_no = 0
        payload_len = 0 
        packet = udpPkt_hdr_data.pack(version, flags, header_len, sequence_no, ack_no, payload_len, msgbuffer)
        messagesize = struct.calcsize(sizeofpkt)
        buffersize = 4096 - messagesize
        destination2, port = address
        global destination
        destination = destination2
        myAddress = (destination, sendPort)
        ackflag = False 
        while ackflag == False:
            try:
                sock.sendto(packet, myAddress)
                print "Client: Waiting for acknowledgement..."
                sock.settimeout(3)
                data, server = sock.recvfrom(messagesize)
                if data:
                    print "Client: RECEIVED ACK "
                    ackflag = True 
                    sizeofpkt2 = '!BBHQQL'
                    version,flag,header_len,sequence_no,ack_no,payload_len=struct.unpack(sizeofpkt2,data)
                    if flag == 4: 
                        print "Client: CONNECTION established..."
            except syssock.timeout:
                print "Socket timed out ..."

    def listen(self,backlog):
        return

    def accept(self):
        global sendPort
        global receivePort
        connectionestablished = False
        firsttry = False
        while connectionestablished == False: 
            print "Server: Waiting...."
            try:    
                msgbuffer = "This is a message from client"
                sock352PktHdrData = '!BBHQQL' + str(len(msgbuffer)) + 's'                
                global sizeofpkt
                sizeofpkt = sock352PktHdrData
                size = struct.calcsize(sizeofpkt)
                myData, address = sock.recvfrom(size)
                global destination
                destination, port = address 
                if myData: 
                    i, sequence_no = self.sock352_get_packet(myData, len(msgbuffer))
                    if i == 1:
                        print "Server: Received connection request"
                        udpPkt_hdr_data = struct.Struct(sizeofpkt)
                        version = 1
                        flags = 4
                        header_len = 0
                        ack_nos = sequence_no
                        sequence_no = sequence_no + 1
                        payload_len = 0
                        msgbuffer = "This is a message from server"
                        sock352PktHdrData = '!BBHQQL' + str(len(msgbuffer)) + 's'
                        sizeofpkt = sock352PktHdrData
                        udpPkt_hdr_data = struct.Struct(sizeofpkt)
                        packet2 = udpPkt_hdr_data.pack(version, flags, header_len, sequence_no, ack_nos, payload_len, msgbuffer)
                        messagesize = sizeofpkt
                        try: 
                        #Causes a connection error 
                            print "Server: SENDING Ack...."
                            sock.sendto(packet2, address)
                            connectionestablished = True 
                            print "Server: CONNECTION established..."
                        except syssock.error, exc: 
                            print "Caught exception error: %s" % exc
            except syssock.error as msg : 
                print "socket failure "
        return (socket(), address)

    def close(self):   # fill in your code here 
        return 



    def send(self,buffer):
        global initflag
        global getpktsize
        if buffer == 4: 
            sock.sendto(buffer, (destination,sendPort))
            return 4
        if len(buffer) == 16:
            sock.sendto(buffer, (destination, sendPort))
            return 16
        if initflag == False: 
                sock.sendto(buffer, (destination,sendPort))
                initflag = True 
                return len(buffer)
        if initflag == True: 
            sock352PktHdrData = '!BBHQQL' + str(len(buffer)) + 's' 
            sizeofpkt = sock352PktHdrData
            getpktsize = sizeofpkt
            udpPkt_hdr_data = struct.Struct(sizeofpkt)
            version = 1
            flags = 32
            header_len = 0
            sequence_no = randomSeq
            ack_no = 0
            payload_len = 0 
            packet = udpPkt_hdr_data.pack(version, flags, header_len, sequence_no, ack_no, payload_len, buffer)
            messagesize = struct.calcsize(sizeofpkt)
            data = 0
            receivedAck = False 
            try: 
                sock.sendto(packet, (destination,sendPort))
                print "Waiting for data acknowledgement..."
                sock.settimeout(.2)
                data, server = sock.recvfrom(messagesize)
                if data:
                    
                    print "Client: Received data ack" 
                    receivedAck = True 
                    bytessent = len(buffer)
            except syssock.timeout:
                print "Timed out .... "
                bytessent = 0 
        if data: 
            return bytessent 


    def recv(self,nbytes):
        global initflag2
        if nbytes == 16: 
            data, server = sock.recvfrom(nbytes)
            return data
        if initflag2 == False: 
            data, server = sock.recvfrom(nbytes) 
            initflag2 = True 
            return data
        if initflag2 == True:          
            bytesreceived = 0     # fill in your code here
            data , address= sock.recvfrom(24 + nbytes)
            bytesreceived=self.sock352_get_packet(data, nbytes)
            #size = '!BBHQQL' + str(nbytes) + 's' 
            #version,flag,header_len,sequence_no,ack_no,payload_len,msgbuffer=struct.unpack(size,data)
            msgbuffsize = len(bytesreceived)
            return bytesreceived
            if msgbuffsize>nbytes:
                print "bytesrecieved too big somehow"
                return None
            return bytesreceived
