
from bootcfgmgr.loaders import Loader, register_loader

import logging
log = logging.getLogger("bootcfgmgr")

class Grub2(Loader):
    """ GRUB 2 """
    _type = "grub2"
    _name = None
    _supported = True
    _arches = [ "x86_64", "i386", "i686", "aarch64", "ppc64", "ppc64le" ]
    _all_config_files = [
            "/etc/grub2-efi.cfg",
            "/etc/grub2.cfg",
            "/boot/grub2/grub.cfg",
            "/boot/grub2-efi/grub.cfg",
            "/boot/grub/grub.cfg",
        ]
    _efi_config_files = [
            "/etc/grub2-efi.cfg",
            "/boot/grub2-efi/grub.cfg",
        ]

    def __init__(self, **kwargs):
        Loader.__init__(self, **kwargs)
        self.forceEfi = False

    @property
    def _config_files(self):
        for x in self._all_config_files:
            if self.forceEfi:
                if x in self._efi_config_files:
                    yield x
            else:
                yield x

register_loader(Grub2)
