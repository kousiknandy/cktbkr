from singleton import Singleton
from datetime import datetime


class CircuitOpenException(Exception):
    pass


class Circuitbreaker(Singleton):
    closed = True
    ts = datetime.now()

    def __new__(cls, name, timeout=5, retries=1):
        it = super().__new__(cls, name)
        it.timeout = timeout
        it.retries = retries
        return it

    def __enter__(self):
        if not getattr(self, "_numtry", None):
            self._numtry = 0
        if self.closed:
            return self
        elapsed = (datetime.now() - self.ts).total_seconds()
        if elapsed > self.timeout:
            self.closed = True
            print("Timeout over, retrying")
            self._numtry = 0
            return self
        print("Circuit open, not allowed")
        raise CircuitOpenException()

    def __exit__(self, extype, exval, extb):
        if not exval:
            return True
        self._numtry += 1
        if self._numtry >= self.retries:
            print(
                f"Exception {extype} {exval}, exceeded {self.retries} opening circuit"
            )
            self.ts = datetime.now()
            self.closed = False
        else:
            print(f"Exception {extype} {exval}, retry count {self._numtry}")
        return True

    def __call__(self, function):
        async def wrapp(*args, **kwargs):
            try:
                with self:
                    return await function(*args, **kwargs)
            except CircuitOpenException:
                pass
            return None

        return wrapp


if __name__ == "__main__":
    x = Circuitbreaker("foo", 100)
    y = Circuitbreaker("foo", 200)
    z = Circuitbreaker("bar")
    assert x is y
    assert x is not z
