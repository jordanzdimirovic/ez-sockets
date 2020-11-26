"""

"""

import time, sys, os, json, threading, socket, binascii
from typing import Dict, Callable

#region Helper Functions
def random_hex(length: int):
    return binascii.b2a_hex(os.urandom(length // 2)).decode()
#endregion

class EZSConnectedClient():
    def __init__(self):
        pass
    def send_data(self):
        pass

class EZSServer():
    def __init__(self):
        self.__threads = {}

        self.__connected_clients = {}

    def listen(self, port: int, callback: Callable, local: bool = False) -> None:
        #region Bind and start listening / heartbeat threads
        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4, TCP

        self.address = ("localhost", "0.0.0.0")[local]

        self.port = port

        self.TCPSOCKET.bind((self.address, self.port))

        self.__threads = {
            "listening": threading.Thread(target=T_get_incoming, daemon=True),
            "heartbeat": threading.Thread(target=T_heartbeat, daemon=True)
        }
        
        for t in self.__threads:
            self.__threads[t].run()

        #endregion

    
    def sendall(self, data: Dict) -> None:
        # Call send_data(data) on all connected clients
        pass

    def T_heartbeat(self) -> None:
        pass

    def T_get_incoming(self) -> None:
    