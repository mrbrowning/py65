import sys

if sys.platform[:3] == "win":
    import msvcrt

    def getch(stdin):
        """ Performs a nonblocking read of one byte from the Windows
        console and returns its ordinal value.  The stdin argument
        is for function signature compatibility and is ignored.  If 
        no byte is available, 0 is returned.
        """
        if msvcrt.kbhit():
            return ord(msvcrt.getch())
        return 0

else:
    import select
    import os
    import termios
    import fcntl

    def getch(stdin):
        """ Performs a nonblocking read of one byte from stdin and returns 
        its ordinal value.  If no byte is available, 0 is returned.
        """
    
        fd = stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = oldterm[:]
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            byte = 0
            r, w, e = select.select([fd], [], [], 0.1)
            if r:
                c = stdin.read(1)
                byte = ord(c)
                if byte == 0x0a:
                    byte = 0x0d
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return byte
