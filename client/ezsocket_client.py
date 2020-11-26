"""

"""

import socket, json

from typing import Dict, Callable

class EZSClient():
    def __T_get_incoming(self):
        

    def __init__(self):
        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_registry = {} # event key -> callable



    def connect(self, ip, port):
        self.server_address = (ip, port)

    def on(self, event: str, callback: Callable):
        self.event_registry[event] = callback
    
    def __handle_event(self, event: str, data: Dict)

    def send(self, key: str, data: Dict):
        pass

    
