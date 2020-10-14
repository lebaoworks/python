class A:
    class X:
        pass
    def Y(self):
        pass
    def Z():
        pass

for key in dir(A):
    if not key.startswith("__") and type(getattr(A,key)) == type:
        print(key)