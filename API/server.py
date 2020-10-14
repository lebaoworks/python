from importlib import import_module, reload

from base.httpserver import HTTPServer, HTTPRequestHandler
from base.api import BaseAPI

import sys
import json

class APIHandler(HTTPRequestHandler):    
    response_headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Methods": "OPTIONS, HEAD, GET, POST, PUT, DELETE",
        "Access-Control-Allow-Headers": "*",
    }

    def execute(self):
        if self.path.startswith("/api/"):
            try:
                api_path = f"api{self.path[4:].replace('/','.')}"
                print(api_path)
                api_module = import_module(api_path)
                api_module = reload(api_module)
                api = getattr(api_module, 'API')()
                self.response_headers.update(api.headers)
                self.response_code, response_data = api.execute(self)
                self.response_data = json.dumps(response_data, ensure_ascii=False).encode('utf-8')            
            except Exception as e:
                print(f"[!] {str(e)}")
                self.response_code, self.response_data = 500, b'{"result":"UNKNOWN_EXCEPTION"}'
        else:
            super().execute()
            
if __name__ == "__main__":
    print(f"""

        WEB SERVICE

    USAGE: {sys.argv[0]} [port (80 as default)]
    """)

    address = ('0.0.0.0', int(sys.argv[1]) if len(sys.argv)==2 else 80)
    print(f"        Starting Server using {address}")
    server = HTTPServer(address, APIHandler)
    server.serve()
