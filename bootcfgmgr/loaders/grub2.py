
from bootcfgmgr.loaders import Loader, register_loader

import logging
log = logging.getLogger("bootcfgmgr")

class Grub2(Loader):
    """ GRUB 2 """
    _type = "grub2"
    _name = None
    _supported = True
    _arches = [ "x86_64", "i386", "i686", "aarch64", "ppc64", "ppc64le" ]
    _config_files = [
            "/etc/grub2-efi.cfg",
            "/etc/grub2.cfg",
            "/boot/grub2/grub.cfg",
            "/boot/grub2-efi/grub.cfg",
            "/boot/grub/grub.cfg",
        ]

register_loader(Grub2)
