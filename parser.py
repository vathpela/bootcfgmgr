#!/usr/bin/python3

import collections
import copy
import functools
import string
import pdb

def tokenize(s):
    token = ""
    if len(s) == 0:
        return []
    for c in s:
        if len(token) == 0:
            token = c
        elif (c in string.whitespace) == (token[0] in string.whitespace):
            token += c
        else:
            yield token
            token = c
    yield token

def isOnlyWhitespace(s):
    for x in str(s):
        if not x in string.whitespace:
            return False
    return True

class ConfigLine(collections.UserList):
    def __init__(self, s):
        self.raw = s
        self.data = list(tokenize(self.raw))
        self.depth = 0
        if len(self) > 0 and isOnlyWhitespace(self.data[0]):
            for c in self.data[0]:
                if c == '\t':
                    self.depth += 8
                else:
                    self.depth += 1

    @property
    def tokens(self):
        return self.data

    @property
    def indents(self):
        if len(self.data) < 1:
            return ""

        if isOnlyWhitespace(self.data[0]):
            return self.data[0]
        return ""

    def __str__(self):
        return "".join(self.data)

    # this is probably wrong to do, but it makes debugging really easy right now
    def __repr__(self):
        return "[%s] %s" % (self.indents, "".join(self.tokens))

class ConfigFile(object):
    def __init__(self, buf):
        self.raw = buf

        self.delimiter = '\n'
        if buf.find('\r\n') != -1:
            self.delimeter = '\r\n'
        lines = buf.splitlines()
        self.lines = []
        for line in lines:
            self.lines.append(ConfigLine(line))

if __name__ == '__main__':
    f = open("grub2-efi.cfg", "r")
    buf = f.read()
    cf = ConfigFile(buf)
