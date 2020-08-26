import socket
import select
import struct
from socketserver import ThreadingTCPServer, StreamRequestHandler

def log_message(text):
    print(text)

def connect_socket(client, remote):
    while True:
        r, w, e = select.select([client, remote], [], [])
        if client in r:
            data = client.recv(4096)
            if remote.send(data) <= 0:
                break
        if remote in r:
            data = remote.recv(4096)
            if client.send(data) <= 0:
                break

class Intermediary(StreamRequestHandler):
    timeout = 5
    username = "xname"
    password = "xpass"

    def auth(self):
        # Recv header
	    #  ---------------------------------
	    #  | VER | NMETHODS | METHODS_LIST |
	    #  ---------------------------------
	    #  |  1  |     1    |   NMETHODS   |
	    #  ---------------------------------

        version, nmethods = self.connection.recv(2)
        if version != 5:
            return False

        # get method list
        methods = [ord(self.connection.recv(1)) for _ in range(0, nmethods)]
        log_message(f"{self.client_address} => METHODS = {methods}")

        if 0 in methods:    #NOAUTH
            log_message(f"{self.client_address} => AUTH: 0 => OK")
            self.connection.send(struct.pack("!BB", 5, 0))
            return True
        if 2 in methods:    #USERPASS
            self.connection.send(struct.pack("!BB", 5, 2))
            
            # Recv USERPASS
            #  ---------------------------------------------------
            #  | VER | NAME_LEN |   NAME   | PASS_LEN |   PASS   |
            #  ---------------------------------------------------
            #  |  1  |     1    | NAME_LEN |     1    | PASS_LEN |
            #  ---------------------------------------------------
            self.connection.recv(1)

            name_len = ord(self.connection.recv(1))
            _name = self.connection.recv(name_len).decode()
            pass_len = ord(self.connection.recv(1))
            _pass = self.connection.recv(pass_len).decode()

            if _name == self.username and _pass == self.password:
                log_message(f"{self.client_address} => AUTH: 2 ({_name}, {_pass}) => OK")
                self.connection.send(struct.pack("!BB", 1, 0))
                return True
            else:
                log_message(f"{self.client_address} => AUTH: 2 ({_name}, {_pass}) => FAIL")
                self.connection.send(struct.pack("!BB", 1, 0xFF))
                return False

        log_message(f"{self.client_address} => AUTH: UNKNOWN => FAIL")
        return False

    def handle_request(self):
        # Recv request
	    #  ---------------------------------------
	    #  | VER | CMD | RSV | TYP | ADDR | PORT |
	    #  ---------------------------------------
	    #  |  1  |  1  |  1  |  1  | Vari |   2  |
	    #  ---------------------------------------

        version, command, reserve, addr_type = self.connection.recv(4)
        if version != 5:
            return False
        
        if addr_type == 1:  # IPv4
            address = socket.inet_ntoa(self.connection.recv(4))
        if addr_type == 3:  # Domain
            addr_len = self.connection.recv(1)
            address = self.connection.recv(addr_len)
        port = int.from_bytes(self.connection.recv(2), byteorder='big')
        log_message(f"{self.client_address} => CMD: {command} TYP: {addr_type} ADDR: {address} PORT: {port}")

        if command == 1:  # establish TCP connection
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((address, port))
            
            # response
            self.connection.send(struct.pack("!BBBB",5, 0, 0, addr_type))
            if addr_type == 1:
                self.connection.send(socket.inet_aton(address))
            if addr_type == 3:
                self.connection.send(struct.pack("!B",len(address)))
                self.connection.send(address.encode())
            self.connection.send(struct.pack("!H", port))

            # connect 2 connections
            connect_socket(self.connection, remote)

    def handle(self):
        log_message(f"[*] => Connection: {self.client_address}")
        if self.auth():
            self.handle_request()
            
if __name__ == '__main__':
    server = ThreadingTCPServer(('0.0.0.0', 9999), Intermediary)
    log_message("=> SOCKS5 Server started")
    server.serve_forever()