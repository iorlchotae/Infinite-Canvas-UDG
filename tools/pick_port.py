"""Pick a free TCP port for the canvas server.

Usage: python pick_port.py [start_port] [max_tries]
Prints the chosen port number to stdout.
Used by start.bat so a new machine where port 3000 is already taken
still gets a working URL instead of a crash.
"""
import socket
import sys


def pick_port(start: int = 3000, tries: int = 20) -> int:
    for port in range(start, start + tries):
        # NOTE: plain bind without SO_REUSEADDR on purpose.
        # On Windows, SO_REUSEADDR lets TWO sockets share one port, which would
        # make a held port look free while uvicorn (exclusive bind) still fails.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    return start


if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(pick_port(start, tries))
