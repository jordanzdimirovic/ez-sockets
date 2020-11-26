"""

"""

import socket, json, threading

from typing import Dict, Callable

class EZSClient():
    def __T_get_incoming(self):
        while self.listening:
            data = self.TCPSOCKET.recv(self.msg_size)
            try:
                data = data.decode()
                event_end = data.find("\n")
                event, content = data[:event_end], data[event_end + 1:].strip()
                if event == "heartbeat":
                    print("♥")
                    continue
                if content.strip() != "": content = json.loads(content)
                else: content = None
                self.__handle_event(event, content)

            except Exception as e:
                print(f"Error on receiving server data:\n{e}")

    def __init__(self):
        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_registry = {} # event key -> callable

    def connect(self, ip, port, msg_size = 1024):
        self.listening = True
        self.msg_size = msg_size
        self.server_address = (ip, port)
        self.TCPSOCKET.connect(self.server_address)
        t = threading.Thread(target=self.__T_get_incoming, daemon=True)
        t.start()

    def on(self, event: str, callback: Callable):
        assert event != "heartbeat"
        self.event_registry[event] = callback
    
    def __handle_event(self, event: str, data: Dict):
        assert event in self.event_registry, "Event not found."
        self.event_registry[event](data)

    def send(self, key: str, data: Dict):
        packet = key + '\n'
        packet += json.dumps(data)
        self.TCPSOCKET.send(packet.encode())

if __name__ == "__main__":
    def count_keys(data):
        for i, k in enumerate(data):
            print(f"{i} - {k}")
        print(f"There were {i+1} values.")
    
    c = EZSClient()
    c.on("test", count_keys)
    c.connect("localhost", 8080)
    input()