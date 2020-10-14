import json
from base.httpserver import HTTPRequestHandler

class BaseAPIMethod:
    # Users = [Role1, Role2]
    Users = [None]
    # Params = [(name, type, 'required'), ]
    Params = []

    def execute(self):
        raise Exception("NOT_DEFINED")

class BaseAPI:
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Methods": "",
        "Access-Control-Allow-Headers": "*",
    }

    def __init__(self):
        if "Access-Control-Allow-Methods" not in self.headers:
            self.headers["Access-Control-Allow-Methods"] = ""
        for key in dir(self):
            if not key.startswith("__") and type(getattr(self, key)) == type:
                self.headers["Access-Control-Allow-Methods"] = ", ".join([self.headers["Access-Control-Allow-Methods"], key])
   
    # Authenticate user's identity
    def authenticate(self, request):
        return None

    def authorize(self, request, api):
        if self.authenticate(request) in api.Users:
            return True
        return False

    # Verify params' type
    def verify(self, request, api):
        for param_name, param_type, required in api.Params:
            if required == "required":
                if param_name not in request.body:
                    return False
                else:
                    if type(request.body[param_name]) != param_type:
                        print(type(request.body[param_name]), param_type)
                        return False
        return True

    def execute(self, request):
        if hasattr(self, request.command):
            api = getattr(self, request.command)
            if self.authorize(request, api):
                if self.verify(request, api):
                    return api.execute(request)
                return 400, "INVALID_SYNTAX"
            return 403, "UNAUTHORIZED"
        return 404, "NOT_SUPPORTED"

    class OPTIONS(BaseAPIMethod):
        Users = [None]
        Params = []
        def execute(request):
            return 200, "OK"
