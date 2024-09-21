""" Read UDP packets and send out on web socket"""
import argparse
import logging
import os
import json
import socket
import struct

from websocket_server import WebsocketServer

CLIENT_LIST = []
SERVER = []


def add_client(client, _):
    """Add client to client list"""
    print("Connecting client at ", client["address"])
    CLIENT_LIST.append(client["address"])


def remove_client(client, _):
    """Remove client from client list"""
    print("Removing client at ", client["address"])
    CLIENT_LIST.remove(client["address"])


def forward_udp(p):
    "Get UDP packets and forward"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    sock.bind(("127.0.0.1", p))
    while True:
        try:
            buf = sock.recv(4096)
            out = {"time": struct.unpack_from("@d", buf, offset=0)}
            n = max(200, len(buf)//8)
            for i in range(1, n):
                out[f"x{i:03d}"] = struct.unpack_from("@d", buf, offset=8*i)

            SERVER.send_message_to_all(json.dumps(out))
        except TimeoutError:
            pass


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Receive UDP packets and forward on websocket")
    parser.add_argument("-p", "--portudp", default=41952,
                        help="Port number, to listen for udp packets"
                        + "default=41952")
    parser.add_argument("-l", "--portweb", default=41953,
                        help="Port number, to listen for websocket connections"
                        + "default=41953")
    args = parser.parse_args()

    # Start websocket server
    SERVER = WebsocketServer(host="127.0.0.1", port=args.portweb,
                             loglevel=logging.INFO)
    SERVER.set_fn_new_client(add_client)
    SERVER.set_fn_client_left(remove_client)
    SERVER.run_forever(threaded=True)

    # Listen for UDP packets and send to websocket
    forward_udp(args.portudp)
