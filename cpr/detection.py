from enum import Enum
import os
import sys
from locale import getpreferredencoding
import mmap

from six import string_types

on_win = sys.platform == "win32"

codec = getpreferredencoding() or 'utf-8'
mmap_MAP_PRIVATE = 0 if on_win else mmap.MAP_PRIVATE
mmap_PROT_READ = 0 if on_win else mmap.PROT_READ
mmap_PROT_WRITE = 0 if on_win else mmap.PROT_WRITE


class FileMode(Enum):
    text = 'text'
    binary = 'binary'

    def __str__(self):
        return "%s" % self.value


def mmap_mmap(fileno, length, tagname=None, flags=0, prot=mmap_PROT_READ | mmap_PROT_WRITE,
              access=None, offset=0):
    '''
    Hides the differences between mmap.mmap on Windows and Unix.
    Windows has `tagname`.
    Unix does not, but makes up for it with `flags` and `prot`.
    On both, the default value for `access` is determined from how the file
    was opened so must not be passed in at all to get this default behaviour.
    '''
    if on_win:
        if access:
            return mmap.mmap(fileno, length, tagname=tagname, access=access, offset=offset)
        else:
            return mmap.mmap(fileno, length, tagname=tagname)
    else:
        if access:
            return mmap.mmap(fileno, length, flags=flags, prot=prot, access=access, offset=offset)
        else:
            return mmap.mmap(fileno, length, flags=flags, prot=prot)


def _ensure_list(arg):
    if (isinstance(arg, string_types) or not hasattr(arg, '__iter__')):
        if arg is not None:
            arg = [arg]
        else:
            arg = []
    return arg


def detect_prefix_files(prefix, files=None, extra_paths=None):
    '''
    Yields files that contain the current prefix in them

    :param files: Filenames to check for instances of prefix
    :type files: list of tuples containing strings (prefix, mode, filename)
    '''

    if not files:
        files = [os.path.relpath(os.path.join(dp, f), prefix)
                 for dp, dn, filenames in os.walk(prefix)
                 for f in filenames]

    paths_to_find = [prefix]
    for p in _ensure_list(extra_paths):
        paths_to_find.append(os.path.normpath(os.path.join(prefix, p)))
    if on_win:
        paths_to_find.extend([prefix.replace('\\', '/'), prefix.replace('\\', '\\\\')])
    binary_paths_to_find = [p.encode(codec) for p in paths_to_find]

    for f in files:
        if f.endswith(('.pyc', '.pyo')):
            continue
        path = os.path.join(prefix, f)
        if not os.path.isfile(path):
            continue
        if sys.platform != 'darwin' and os.path.islink(path):
            # OSX does not allow hard-linking symbolic links, so we cannot
            # skip symbolic links (as we can on Linux)
            continue

        # dont try to mmap an empty file
        if os.stat(path).st_size == 0:
            continue

        try:
            fi = open(path, 'rb+')
        except IOError:
            continue
        try:
            mm = mmap_mmap(fi.fileno(), 0, tagname=None, flags=mmap_MAP_PRIVATE)
        except OSError:
            mm = fi.read()

        mode = 'binary' if mm.find(b'\x00') != -1 else 'text'
        for path in binary_paths_to_find:
            if mm.find(path) != -1:
                yield (prefix, mode, f)
        mm.close()
        fi.close()
