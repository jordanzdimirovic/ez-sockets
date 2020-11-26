"""
EZ Socket Server for Python

Jordan Zdimirovic - 
"""

import time, sys, os, json, threading, socket, binascii
from typing import Dict, Callable

#region Helper Functions
def random_hex(length: int):
    return binascii.b2a_hex(os.urandom(length // 2)).decode()
#endregion

class EZSConnectedClient():
    def __init__(self, server, address):
        self.server = server

        
    def send(self, data):
        pass

    def disconnect(self):
        pass    

class EZSServer():
    def __init__(self):
        self.listening = False
        
        self.__threads = {}

        self.__connected_clients = {}

    def __T_heartbeat(self) -> None:
        pass

    def __T_get_incoming(self) -> None:
        while self.listening:
            try:
                data, addr = self.TCPSOCKET.recvfrom(self.msg_size)
                print(addr)
            except socket.timeout:
                pass

    def listen(self, port: int, callback: Callable, local: bool = False, msg_size = 1024, recv_timeout = 1) -> None:
        #region Bind and start listening / heartbeat threads
        self.listening = True

        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4, TCP

        self.TCPSOCKET.settimeout(recv_timeout)

        self.msg_size = msg_size

        self.address = ("0.0.0.0", "localhost")[local]

        self.port = port

        self.TCPSOCKET.bind((self.address, self.port))

        self.TCPSOCKET.connect(("localhost", self.port))

        self.__threads = {
            "listening": threading.Thread(target=self.__T_get_incoming, daemon=True),
            "heartbeat": threading.Thread(target=self.__T_heartbeat, daemon=True)
        }
        
        for t in self.__threads:
            self.__threads[t].start()
        
        #endregion

    def __sendtoaddr(self, data: bytes, addr) -> None:
        self.TCPSOCKET.sendto(data, addr)

    def broadcast(self, data: Dict) -> None:
        # Call send_data(data) on all connected clients
        for c in self.__connected_clients:
            self.__connected_clients[c].send(data)

    

if __name__ == "__main__":
    s = EZSServer()
    s.listen(8080, None)
    
    while True:
        x = input(" => ").strip().lower()
        if x == "c":
            sys.exit()
            quit()

