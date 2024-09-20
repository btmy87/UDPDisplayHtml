"""source for UDP packets"""
import argparse
import math
import os
import socket
import time

import numpy as np


TIME_PRINT = 1.0
NPRINT = 50


def send_packets(dest, nvals, dt):
    """send packets of given size at given interval"""

    # open a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # infinite loop
    t = 0.0
    t_last_print = t
    n = 0

    offset = np.linspace(0, 1, nvals)
    while True:
        # make a packet
        t += dt
        vals = np.sin(0.2*t + offset)
        buf = vals.tobytes()
        sock.sendto(buf, dest)
        time.sleep(dt)
        # print("Sending packet at t = ", t)

        if t >= (t_last_print + TIME_PRINT):
            n += 1
            t_last_print = t
            print(".", end="", flush=True)

        if n > NPRINT:
            n = 0
            print("")


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Generates UDP packets for testing display")
    parser.add_argument("-p", "--port",
                        default=41952,
                        help="Port number, destination, default=41952")
    parser.add_argument("-a", "--address",
                        default="127.0.0.1",
                        help="IP Address, destination, default=127.0.0.1")
    parser.add_argument("-n", "--numbytes",
                        default=1600,
                        help="Number of bytes in packet, "
                        + "will be rounded down to a multiple of 8 bytes, "
                        + "default=1600")
    parser.add_argument("-t", "--timeinterval",
                        default=0.01,
                        help="Time interval for sending packets, seconds, default=0.01")

    args = parser.parse_args()
    dest_addr = (args.address, args.port)
    nvals_packet = math.floor(args.numbytes/8)

    # run stuff
    print(f"Sending packets to {dest_addr}")
    send_packets(dest_addr, nvals_packet, args.timeinterval)
