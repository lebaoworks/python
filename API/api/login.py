from base.api import BaseAPI, BaseAPIMethod

class API(BaseAPI):
    class POST(BaseAPIMethod):
        Users = [None]
        Params = [
            ('username', str, 'required'),
            ('password', str, 'required')
        ]
        def execute(request):
            if request.body['username'] == 'ADMIN' and request.body['password'] == "122":
                return 200, "OK"
            return 401, "FAIL"

