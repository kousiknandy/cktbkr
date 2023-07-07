from  singleton import Singleton
from datetime import datetime

class CircuitOpenException(Exception):
    pass

class Circuitbreaker(Singleton):
    closed = True
    ts = datetime.now()

    def __enter__(self):
        if self.closed: return
        elapsed = (datetime.now() - self.ts).total_seconds()
        if elapsed > 5:
            self.closed = True
            return
        raise CircuitOpenException()

    def __exit__(self, extype, exval, extb):
        if not exval: return True
        self.ts = datetime.now()
        self.closed = False
        return True
        

if __name__ == "__main__":
    x = Circuitbreaker("foo", 100)
    y = Circuitbreaker("foo", 200)
    z = Circuitbreaker("bar")
    assert x is y
    assert x is not z
