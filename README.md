pyadbfs
=======

Warning: Incompleted, abandoned.

FUSE based filesystem for mounting Android devices using Android Debugging Bridge built with fuse.py.

I started writing this because my device doesn't support USB Mass Storage and I couldn't manage any of the MTP bindings([jmtpfs][], [go-mtpfs][], [simple-mtpfs][]) work, also ADB can work wirelessly too.

But now I abandoned this project, instead installed a SSH Server on my phone and started using SSHFS.

Note: fuse.py(https://github.com/terencehonles/fusepy) is included in project because I used 2to3 on it, probably it's best to use latest version from there.

What Works
----------

* Mounting read-only(`./pyadbfs.py mount_dir`).
* Listing directories(`ls -l`) and symlink handling.
* stat(Just a few attributes(atime, mtime, size, uid,gid))
* reading files(Losts a few bytes, don't know why, buggy and horribly slow, I'm probably using the worst way.)

What Doesn't Work
-----------------
* Useful things, like reading and writing files,
* chmod, chown, rm etc...
* Pretty much everything else.

TODO
----

* Fix the memoization on stat command, I don't even know if it works; I think the best way is fetch whole directory contents with a wildcard, and fetch from it).
* Think something less embarrassing for read command.

[jmtpfs]: https://github.com/kiorky/jmtpfs
[simple-mtpfs]: https://github.com/phatina/simple-mtpfs
[go-mtpfs]: https://github.com/hanwen/go-mtpfs
    
