

from . import Loader, register_loader

import logging
log = logging.getLogger("bootcfgmgr")

class Grub2(Loader):
    """ GRUB 2 """
    _type = grub2
    _name = None
    _supported = True

register_loader(Grub2)
