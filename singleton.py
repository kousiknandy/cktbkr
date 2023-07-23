class Singleton(object):
    """Ensure there is a single instance of this class
    we intercept the new() and check our vault for an
    existing instance, if not create it and put in vault"""
    def __new__(cls, name, /, *args, **kwargs):
        vlt = cls.__dict__.get("__vault__")
        if not vlt:
            cls.__vault__ = {}
        if it := cls.__vault__.get(name):
            return it
        it = cls.__vault__[name] = object.__new__(cls)
        return it
