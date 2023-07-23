class Singleton(object):
    def __new__(cls, name, /, *args, **kwargs):
        vlt = cls.__dict__.get("__vault__")
        if not vlt:
            cls.__vault__ = {}
        if it := cls.__vault__.get(name):
            return it
        it = cls.__vault__[name] = object.__new__(cls)
        return it
