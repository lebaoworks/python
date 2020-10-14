from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, unquote
import socket
import json

class HTTPRequestHandler(BaseHTTPRequestHandler):
    response_headers = {
        "Content-type": "*/*",
        "Access-Control-Allow-Methods": "GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH",
    }

    # Hide log message on server
    def log_message(*args, **kwargs):
        pass

    # Parse request
    def parse_request(self):
        # Default parser
        if not super().parse_request():
            return False
        try:
            # Parse cookie
            self.cookie = SimpleCookie(self.headers['Cookie'])

            # Parse body
            self.body = {}
            if self.command == "GET":
                self.body = dict((k,v[-1]) for k,v in parse_qs(urlparse(self.path).query).items())
            if self.command in ["POST", "PUT"]:
                raw = self.rfile.read(int(self.headers['Content-Length']))
                if "application/json" in self.headers['Content-Type']:
                    self.body = json.loads(raw.decode())
                if "application/x-www-form-urlencoded" in self.headers['Content-Type']:
                    self.body = dict((k,v[-1]) for k,v in parse_qs(raw.decode()).items())
            
            # Idealize path
            self.path = unquote(urlparse(self.path).path)
        except:
            return False
        return True

    # Execute method
    def execute(self):
        method = getattr(self, self.command)
        self.response_code, self.response_data = method()
    
    # Response
    def respond(self):
        self.send_response(self.response_code)
        for key, value in self.response_headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(self.response_data)
        self.wfile.flush() #actually send the response if not already done.

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            self.command = self.command.upper()
            self.execute()
            self.respond()
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return        
        except Exception as e:
            print(e)

    def GET(self):
        return 404, b''
    
    def HEAD(self):
        return 200, b''

    def POST(self):
        return 404, b''

    def PUT(self):
        return 404, b''
    
    def DELETE(self):
        return 404, b''
    
    def CONNECT(self):
        return 404, b''

    def OPTIONS(self):
        return 200, b''
    
    def TRACE(self):
        return 404, b''

    def PATCH(self):
        return 404, b''

class HTTPServer:
    def __init__(self, address, handler):
        self.httpd = ThreadingHTTPServer(address, handler)
    def serve(self):
        self.httpd.serve_forever()
