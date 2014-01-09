#!/usr/bin/env python3

import sys
import time
import subprocess

import fuse

class ADB:
    class ADBShell:
        def __getattr__(self, name):
            return self[name]
        def __getitem__(self, cmd):
            return self.raw(cmd).strip().decode()
        def raw(self, cmd):
            print("! %s" % cmd)
            out = subprocess.check_output(["adb", "shell", cmd])
            return out

    def __init__(self):
        if not self._connected:
            raise IOError("Can't find device")

    @property
    def _connected(self):
        status = subprocess.Popen(["adb", "get-state"], 
                    stdout=subprocess.PIPE).communicate()[0]
        return status.decode().strip() == "device"


class ADBFS(fuse.LoggingMixIn, fuse.Operations): 
    def __init__(self, adb):
        self.adb = adb
        self._stat_memoize = {}

    def readdir(self, path, fh):
        return self.adb.shell["ls '%s'" % path].splitlines()

    def getattr(self, path, fh):
        if path in self._stat_memoize and self._stat_memoize[path][0] >= time.time() - 1:
            return self._stat_memoize[path][1]

        ret = self.adb.shell["stat -c '%X %Y %u %g %d %i %f %s' " + "'%s'" % path]

        try:
            atime, mtime, uid, gid, dev, ino, mode, size = ret.split()
        except ValueError:
            raise fuse.FuseOSError(fuse.ENOENT)
        else:
            d = {"st_atime": int(atime),
                 "st_mtime": int(mtime),
                 "st_uid": int(uid),
                 "st_gid": int(gid),
                 "st_mode": int(mode, 16),
                 "st_size": int(size),
                 "st_dev": int(dev),
                 "st_ino": int(ino)}
            self._stat_memoize[path] = [time.time(), d]
            return d

    def readlink(self, path):
        return self.adb.shell["readlink %s" % path]

    def read(self, path, size, offset, fh):
        print(offset, size)
        ret = self.adb.shell.raw(
                "dd if='%s' ibs=1 skip=%d count=%d 2>/dev/null" % (path, offset, size)
                )
        print(len(ret))
        return ret

    def __getattr__(self, name):
        print("Called method: %s" % name)
        raise AttributeError()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s <mountpoint>' % sys.argv[0])
        exit(1)

    fuse = fuse.FUSE(
                ADBFS(ADB()), 
                sys.argv[1], 
                foreground=True, 
                nothreads=True)
