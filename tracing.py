"""
For more informations:
    trace_function's args: <https://docs.python.org/3/library/sys.html#sys.setprofile>
    frame: <https://docs.python.org/3/library/inspect.html> 
"""
import sys,os

class Tracing:
    PJ_PATH = os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def stringify_call(frame, with_args=False):
        if frame.f_back == None:
            return ""
        
        if with_args==True:
            args = []
            for arg_name in frame.f_code.co_varnames[:frame.f_code.co_argcount]:
                try:
                    arg_value = str(frame.f_locals[arg_name])[:5]
                except:
                    arg_value = frame.f_locals[arg_name].__class__.__name__
                args.append(arg_name+"="+arg_value)

        return "%s:%d %s(%s)"% (
            os.path.basename(frame.f_back.f_code.co_filename),  #Caller file name
            frame.f_back.f_lineno,                              #Caller line
            frame.f_code.co_name,                               #Callee function name
            ', '.join(args) if with_args else ""                #Callee Arguments
        )

    @staticmethod
    def get_depth(frame):
        i = 0
        while frame.f_back:
            frame = frame.f_back
            i+=1
        return i

    @staticmethod
    def _is_tracing_obj(frame):
        #Ignore any file outside the project
        if not frame.f_code.co_filename.startswith(Tracing.PJ_PATH):
            return False
        #Ignore things like <freeze importlib...>
        if not os.path.isfile(frame.f_code.co_filename):
            return False
        if __file__ == frame.f_code.co_filename:
            return False
        return True

    @staticmethod
    def _tracefunc(frame, event, arg):
        if not Tracing._is_tracing_obj(frame):
            return
        if event == "call":
            print(Tracing.get_depth(frame)*"  " +"-> "+Tracing.stringify_call(frame))
        if event == "return":
            print(Tracing.get_depth(frame)*"  " +"<- "+str(arg)[:5])
        return

sys.setprofile(Tracing._tracefunc)

