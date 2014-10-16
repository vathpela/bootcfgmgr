import functools
import itertools

class ObjectID(object):
    """This class is meant to be extended by other classes which require
       an ID which is preserved when an object copy is made.
       The value returned by the builtin function id() is not adequate:
       that value represents object identity so it is not in general
       preserved when the object is copied.

       The name of the identifier property is id, its type is int.

       The id is set during creation of the class instance to a new value
       which is unique for the object type. Subclasses can use self.id during
       __init__.
    """

    _newid_gen = functools.partial(next, itertools.count())

    def __new__(cls, *args, **kwargs):
        self = super(ObjectID, cls).__new__(cls, *args, **kwargs)
        self.id = self._newid_gen() # pylint: disable=attribute-defined-outside-init
        return self


