"""
EZ Socket Server for Python

Jordan Zdimirovic - https://github.com/jordstar20001/ez-sockets.git
"""

import time, sys, os, json, threading, socket, binascii
from typing import Dict, Callable

#region Helper Functions
def random_hex(length: int):
    return binascii.b2a_hex(os.urandom(length // 2)).decode()
#endregion

class EZSConnectedClient():
    def __init__(self, server, sock, address):
        self.sock = sock
        self.address = address
        self.server = server

    def send(self, key: str, data: Dict):
        packet = key + '\n'
        packet += json.dumps(data)
        self.sock.send(packet.encode())

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
            sock, addr = self.TCPSOCKET.accept()
            print("Accepted.")
            token = random_hex(16)
            self.__connected_clients[token] = EZSConnectedClient(self, sock, addr)
            self.__threads[token] = threading.Thread(target=self.__T_client, args=(sock, addr))
    
    def get_clients(self):
        return self.__connected_clients

    def __T_client(self, client_sock, addr):
        while True:
            print(client_sock)
            print(addr)
            time.sleep(1)
        pass

    def listen(self, port: int, callback: Callable, local: bool = False, msg_size = 1024, recv_timeout = 1, max_connections = 50) -> None:
        #region Bind and start listening / heartbeat threads
        self.listening = True

        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4, TCP
        
        #self.TCPSOCKET.settimeout(recv_timeout)

        self.msg_size = msg_size

        self.address = (socket.gethostname(), "localhost")[local]

        self.port = port

        self.TCPSOCKET.bind((self.address, self.port))

        self.TCPSOCKET.listen(max_connections)

        #self.TCPSOCKET.connect(("localhost", self.port))

        self.__threads = {
            "listening": threading.Thread(target=self.__T_get_incoming, daemon=True),
            "heartbeat": threading.Thread(target=self.__T_heartbeat, daemon=True)
        }
        
        for t in self.__threads:
            self.__threads[t].start()
        
        #endregion

    def broadcast(self, data: Dict) -> None:
        # Call send_data(data) on all connected clients
        for c in self.__connected_clients:
            self.__connected_clients[c].send(data)

    

if __name__ == "__main__":
    s = EZSServer()
    s.listen(8080, None, local=True)
    
    while True:
        x = input(" => ").strip().lower()
        if x.split()[0] == "send":
            client = s.get_clients()[list(s.get_clients().keys())[0]]
            client.send("test", {
                "data": "yes",
                "more": 10
            })
        elif x == "exit":
            sys.exit()
            quit()

