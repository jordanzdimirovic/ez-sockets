"""

"""

import socket, json, threading

from typing import Dict, Callable

DEBUG = True

#region Helpers
def get_event_and_content(data):
    event_end = data.find("\n")
    event, content = data[:event_end], data[event_end + 1:].strip()
    if content.strip() != "": content = json.loads(content)
    else: content = None
    return (event, content)
#endregion

class EZSClient():
    def __T_get_incoming(self):
        while self.listening:
            try:
                data = self.TCPSOCKET.recv(self.msg_size)
                if data == b'':
                    # The socket has been disconnected.
                    self.shutdown()
                    return
                try:
                    data = data.decode()
                    event, content = get_event_and_content(data)
                    
                    self.__handle_event(event, content)

                except Exception as e:
                    if DEBUG: print(f"Format of data was incorrect and subsequently caused an error:\n{e}")

            except Exception as e:
                if DEBUG: print(f"Error when receiving data:\n{e}")
                self.shutdown()
                return


    def __init__(self):
        self.TCPSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_registry = {} # event key -> callable
        self.disconnect_callback = None

    def shutdown(self):
        self.listening = False
        if self.disconnect_callback: self.disconnect_callback()
        # Do anything else that is necessary

    def connect(self, ip, port, msg_size = 1024, disconnect_callback = None):
        self.listening = True
        self.msg_size = msg_size
        self.server_address = (ip, port)
        self.TCPSOCKET.connect(self.server_address)
        self.disconnect_callback = disconnect_callback
        t = threading.Thread(target=self.__T_get_incoming, daemon=True)
        t.start()

    def on(self, event: str, callback: Callable):
        self.event_registry[event] = callback
    
    def __handle_event(self, event: str, data: Dict):
        assert event in self.event_registry, f"Event {event} not found."
        self.event_registry[event](data)

    def send(self, key: str, data: Dict = None):
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
    c.send("smile", {"name": "Jordan"})
    input()