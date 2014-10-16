#!/bin/bash
PYTHONPATH=$PWD exec ./tools/bootcfgmgr --config-file=$PWD/data/grub2-efi.cfg --default-kernel "$@"
