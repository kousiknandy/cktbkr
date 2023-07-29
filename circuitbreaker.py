from enum import Enum
from singleton import Singleton
from datetime import datetime

Circuitstate = Enum("Circuitstate", ["CLOSED", "OPEN", 'HALFOPEN'])

class CircuitOpenException(Exception):
    pass


class Circuitbreaker(Singleton):
    """Circuitbreaker is singleton because if multiple functions are decorated
    with the same name, they should refer to the same circuit breaker, the name
    can be just an arbitrary string chosen by functions, or the hostname or url"""
    state = Circuitstate.CLOSED
    ts = datetime.now()

    def __new__(cls, name, timeout=None, retries=None):
        """Since the first invocation matters we ignore any paramters once set"""
        it = super().__new__(cls, name)
        it.timeout = getattr(it, "timeout", None) or timeout or 5
        it.retries = getattr(it, "retries", None) or retries or 2
        return it

    def __enter__(self):
        if not getattr(self, "_numtry", None):
            self._numtry = 0
        if self.state == Circuitstate.CLOSED:
            return self
        # broken circuit, if waited long enough then retry
        elapsed = (datetime.now() - self.ts).total_seconds()
        if elapsed > self.timeout:
            self.state = Circuitstate.HALFOPEN
            print("Timeout over, retrying as half open")
            self._numtry = self.retries
            return self
        print("Circuit open, not allowed")
        raise CircuitOpenException()

    def __exit__(self, extype, exval, extb):
        if not exval:
            if self.state ==  Circuitstate.HALFOPEN:
                self.state =  Circuitstate.CLOSED
            self._numtry = 0
            return True
        # we're here because of exception, if enough failed, break
        self._numtry += 1
        if self._numtry >= self.retries:
            print(
                f"Exception {extype}, {self._numtry} exceeded {self.retries} opening circuit"
            )
            self.ts = datetime.now()
            self.state = Circuitstate.OPEN
        else:
            print(f"Exception {extype} {exval}, retry count {self._numtry}")
        return True

    def __call__(self, function):
        """When a function is wrapped, we use the context manager ourselves"""
        async def wrapp(*args, **kwargs):
            try:
                with self:
                    return await function(*args, **kwargs)
            except CircuitOpenException:
                pass
            return None

        return wrapp


if __name__ == "__main__":
    x = Circuitbreaker("foo")
    y = Circuitbreaker("foo", 4)
    z = Circuitbreaker("bar")
    assert x is y
    print(x.timeout, y.timeout)
    assert x is not z
