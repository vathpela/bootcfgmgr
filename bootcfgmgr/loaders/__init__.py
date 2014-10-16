
from bootcfgmgr.util import ObjectID
from bootcfgmgr import parser
import os
import importlib
import logging
log = logging.getLogger("bootcfgmgr")

loaders = {}
def register_loader(loader_class):
    if not issubclass(loader_class, Loader):
        raise ValueError("arg1 must be a subclass of Loader")

    loaders[loader_class._type] = loader_class
    log.debug("registered loader class %s as %s" % (loader_class.__name__,
                                                    loader_class._type))

def getLoader(loader_type, *args, **kwargs):
    """ Return an instance of the appropriate Loader class.

        :param loader_type: The name of the loader type
        :type loader_type: str.
        :return: the format instance
        :rtype: :class:`Loader`
        :raises: ValueError
    """
    loader_class = get_loader_class(loader_type)
    if not loader_class:
        loader_class = Loader
    loader = loader_class(*args, **kwargs)

    # this allows us to store the given type for loaders we implement as
    # Loader
    if loader_class and loader.type is None:
        # unknown type, but we can set the name of the format
        loader._name = loader_type

    log.debug("getLoader('%s') returning %s instance with object_id %d",
        loader_type, loader.__class__.__name__, loader.id)
    return loader

def collect_loader_classes():
    """ Pick up all loader classes from this directory.

        note: Modules must call :func:`register_loader` to make
        classes available to :func:`getLoader`
    """
    mydir = os.path.dirname(__file__)
    myfile = os.path.basename(__file__)
    (myfile_name, _ext) = os.path.splitext(myfile)
    for module_file in os.listdir(mydir):
        (mod_name, ext) = os.path.splitext(module_file)
        if ext == '.py' and mod_name != myfile_name:
                importlib.invalidate_caches()
                globals()[mod_name] = __import__("bootcfgmgr.loaders." + mod_name, globals(), locals(), [], 0)

def get_loader_class(loader_type):
    """ Return an appropriate loader class.

        :param loader_type: The name of the loader type.
        :type loader_type: str.
        :returns: The chosen Loader class
        :rtype: class.

        Returns None if no class is found for loader_type.
    """
    if not loaders:
        collect_loader_classes()

    loader = loaders.get(loader_type)
    if not loader:
        for loader_class in loaders.values():
            if loader_type and loader_type == loader_class._name:
                loader = loader_class
                break

    return loader

class Loader(ObjectID):
    """ Generic loader """

    _type = None
    _name = "Unknown"
    _supported = False
    _arches = []
    _config_files = []

    def __init__(self, **kwargs):
        ObjectID.__init__(self)
        self.configFileName = None
        self.configFile = None

    def __repr__(self):
        s = ("%(classname)s instance (%(id)s) object id %(object_id)d--\n"
             "  type = %(type)s  name = %(name)s\n" %
             {"classname": self.__class__.__name__, "id": "%#x" % id(self),
              "object_id": self.id,
              "type": self.type, "name": self.name})
        return s

    @property
    def desc(self):
        return str(self.type)

    def __str__(self):
        return self.desc

    @property
    def name(self):
        if self._name:
            name = self._name
        else:
            name = self.type
        return name

    @property
    def type(self):
        return self._type

    @property
    def compatible(self):
        uname = os.uname()
        if uname.machine in self._arches:
            return True
        return False

    def find_config(self, configFile=None):
        if configFile is None:
            for x in self._config_files:
                print("x: %s" % (x,))
                if os.access(x, os.R_OK|os.W_OK):
                    self.configFileName = x
                    while True:
                        link = self.configFileName
                        try:
                            link = os.readlink(link)
                            self.configFileName = link
                        except:
                            break
                    break
        else:
            if os.access(configFile, os.R_OK|os.W_OK):
                self.configFileName = configFile
                while True:
                    link = self.configFileName
                    try:
                        link = os.readlink(link)
                        self.configFileName = link
                    except:
                        break
            else:
                sys.stderr.write("Could not access config file \"%s\"\n",
                                 configFile)
                raise ValueError(configFile)

        if not self.configFileName:
            return False

        buf = open(self.configFileName, "r").read()
        self.configFile = parser.ConfigFile(buf)
        return True

    @property
    def stanzas(self):
        if not self.configFile:
            return []
        return []

collect_loader_classes()
