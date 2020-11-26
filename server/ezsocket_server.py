"""
EZ Socket Server for Python

Jordan Zdimirovic - https://github.com/jordstar20001/ez-sockets.git
"""

import time, sys, os, json, threading, socket, binascii, timeit
from typing import Dict, Callable

#region Helper Functions
def random_hex(length: int):
    return binascii.b2a_hex(os.urandom(length // 2)).decode()
def dict2tup(d):
    return [(k, d[k]) for k in d.keys()]
def secs2timestr(seconds):
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60
    number_word_pairs = [(hours, "hrs"), (minutes, "mins"), (seconds, "secs")]
    return ", ".join([f"{number} {word}" for number, word in number_word_pairs])
#endregion

class EZSConnectedClient():
    def __init__(self, server, ident, sock, address):
        self.sock = sock
        assert type(sock) == socket.socket
        self.id = ident
        self.address = address
        self.server = server
        print(type(sock))
        self.connect_time = int(timeit.default_timer())
        

    def send(self, key: str, data: Dict = None):
        packet = key + '\n'
        if data:
            packet += json.dumps(data)
        self.sock.send(packet.encode())

    def age(self):
        return timeit.default_timer() - self.connect_time

    def __str__(self):
        return f"Client: {self.id}, connected {secs2timestr(int(self.age()))} ago."

class EZSServer():
    def __init__(self):
        self.listening = False
        
        self.__threads = {}

        self.__connected_clients = {}

    def __T_heartbeat(self, timeout) -> None:
        while self.listening:
            time.sleep(timeout)
            for _, client in self.get_clients():
                try:
                    client.send("heartbeat")
                except:
                    # Assuming that the client has disconnected.
                    self.disconnect_client(client.id)

    def __T_get_incoming(self) -> None:
        while self.listening:
            sock, addr = self.TCPSOCKET.accept()
            print("Accepted.")
            token = random_hex(16)
            self.__connected_clients[token] = EZSConnectedClient(self, token, sock, addr)
            self.__threads[token] = threading.Thread(target=self.__T_client, args=(sock, addr))
    
    def get_clients(self):
        return dict2tup(self.__connected_clients)

    def disconnect_client(self, ident):
        del self.__connected_clients[ident]

    def __T_client(self, client_sock, addr):
        while True:
            print(client_sock)
            print(addr)
            time.sleep(1)
        pass

    def listen(self, port: int, callback: Callable, local: bool = False, msg_size = 1024, recv_timeout = 1, max_connections = 50, heartbeat_timeout = 3) -> None:
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
            "heartbeat": threading.Thread(target=self.__T_heartbeat, daemon=True, args=(heartbeat_timeout,))
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
            client = s.get_clients()[0][1]
            client.send("test", {
                "data": "yes",
                "more": 10
            })
        elif x == "exit":
            sys.exit()
            quit()
        elif x == "clients":
            for i, c in enumerate(s.get_clients()):
                print(f"#{i+1}: {str(c[1])}")

