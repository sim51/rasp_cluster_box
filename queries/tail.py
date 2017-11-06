""" 
  Simple python implementation of tail -f, utilizing inotify. 
  http://stackoverflow.com/questions/1475950/tail-f-in-python-with-no-time-sleep
  ----
  for data in follow(args.filename.encode()):
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
  ----      
"""

import ctypes
from errno import errorcode
import os
from struct import Struct

# constants from <sys/inotify.h>
IN_MODIFY = 2
IN_DELETE_SELF = 1024
IN_MOVE_SELF = 2048


def follow(filename, blocksize=8192):
    """
    Monitors the file, and yields bytes objects.

    Terminates when the file is deleted or moved.
    """
    with INotify() as inotify:
        # return when we encounter one of these events.
        stop_mask = IN_DELETE_SELF | IN_MOVE_SELF

        inotify.add_watch(filename, IN_MODIFY | stop_mask)

        # we have returned this many bytes from the file.
        filepos = 0
        while True:
            with open(filename, "rb") as fileobj:
                fileobj.seek(filepos)
                while True:
                    data = fileobj.read(blocksize)
                    if not data:
                        break
                    filepos += len(data)
                    yield data

            # wait for next inotify event
            _, mask, _, _ = inotify.next_event()
            if mask & stop_mask:
                break

LIBC = ctypes.CDLL("libc.so.6")


class INotify:
    """ Ultra-lightweight inotify class. """
    def __init__(self):
        self.fd = LIBC.inotify_init()
        if self.fd < 0:
            raise OSError("could not init inotify: " + errorcode[-self.fd])
        self.event_struct = Struct("iIII")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self.close()

    def close(self):
        """ Frees the associated resources. """
        os.close(self.fd)

    def next_event(self):
        """
        Waits for the next event, and returns a tuple of
        watch id, mask, cookie, name (bytes).
        """
        raw = os.read(self.fd, self.event_struct.size)
        watch_id, mask, cookie, name_size = self.event_struct.unpack(raw)
        if name_size:
            name = os.read(self.fd, name_size)
        else:
            name = b""

        return watch_id, mask, cookie, name

    def add_watch(self, filename, mask):
        """
        Adds a watch for filename, with the given mask.
        Returns the watch id.
        """
        if not isinstance(filename, bytes):
            raise TypeError("filename must be bytes")
        watch_id = LIBC.inotify_add_watch(self.fd, filename, mask)
        if watch_id < 0:
            raise OSError("could not add watch: " + errorcode[-watch_id])
        return watch_id


def main():
    """ CLI """
    from argparse import ArgumentParser
    cli = ArgumentParser()
    cli.add_argument("filename")
    args = cli.parse_args()
    import sys
    


 
