"""
EZ Socket Server for Python

Jordan Zdimirovic - https://github.com/jordstar20001/ez-sockets.git
"""

import time, sys, os, json, threading, socket, binascii, timeit
from typing import Dict, Callable

DEBUG = True

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
def get_event_and_content(data):
    event_end = data.find("\n")
    event, content = data[:event_end], data[event_end + 1:].strip()
    if content.strip() != "": content = json.loads(content)
    else: content = None
    return (event, content)
#endregion

class EZSConnectedClient():
    def __init__(self, server, ident, sock, address):
        self.sock = sock
        assert type(sock) == socket.socket, "Argument 'socket' must be a valid socket."
        self.id = ident
        self.address = address
        self.server = server
        self.connected = True
        self.connect_time = int(timeit.default_timer())

    def send(self, key: str, data: Dict = None):
        packet = key + '\n'
        if data:
            packet += json.dumps(data)
        try:
            self.sock.send(packet.encode())
        except ConnectionResetError:
            self.server.disconnect_client(self.id)

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.connected = False

    def age(self):
        return timeit.default_timer() - self.connect_time

    def __str__(self):
        return f"Client: {self.id}, connected {secs2timestr(int(self.age()))} ago."

class EZSServer():
    def __init__(self):
        self.listening = False
        
        self.__threads = {}

        self.__connected_clients = {}

        self.event_registry = {}

    def __T_get_incoming(self) -> None:
        while self.listening:
            sock, addr = self.TCPSOCKET.accept()
            print("Accepted.")
            token = random_hex(16)
            client = EZSConnectedClient(self, token, sock, addr)
            self.__connected_clients[token] = client
            self.__threads[token] = threading.Thread(target=self.__T_client, args=(client,))
            self.__threads[token].start()
    
    def on(self, event, callback):
        # TODO assert function signature
        self.event_registry[event] = callback

    def get_clients(self):
        return dict2tup(self.__connected_clients)

    def disconnect_client(self, ident):
        self.__connected_clients[ident].disconnect()
        del self.__connected_clients[ident]

    def disconnect_all(self):
        for c, _ in self.get_clients():
            self.disconnect_client(c)

    def __T_client(self, client):
        while client.connected:
            try:
                data = client.sock.recv(self.msg_size)
                data = data.decode()
                
                try:
                    event, content = get_event_and_content(data)
                except:
                    if DEBUG:
                        print("Data sent was in the incorrect format. Parsing to JSON failed.")

                if event in self.event_registry:
                    self.event_registry[event](client, content)
            except:
                if DEBUG: print(f"Client {client.id} lost connection.")
                if client.connected:
                    self.disconnect_client(client.id)

    def listen(self, port: int, local: bool = False, msg_size = 1024, recv_timeout = 1, max_connections = 50) -> None:
        #region Bind and start listening
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
            "listening": threading.Thread(target=self.__T_get_incoming, daemon=True)
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
    
    def smile_callback(client, data):
        print(f"☺ - Hi there, {data['name']} How are you today?")

    s.on("smile", smile_callback)
    
    s.listen(8080, local=True)

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
        elif x == "disconnect":
            s.disconnect_client(s.get_clients()[0][0])

