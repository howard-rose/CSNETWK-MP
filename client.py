"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file contains the Client class.
An instance of the Server must be running before any Client can connect.
"""

import socket
import threading


class Client:
    """
    This class represents a Client that will connect to a Server.
    The purpose of the client is to request files from the server as well as
    to send files to the server.

    The client will be able to handle multiple servers at once.
    :param host: The host name of the server to connect to.
    :param port: The port number of the server to connect to.
    """

    # Store the current connection to the server
    connection = None

    def __init__(self, host, port):
        # Create a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.socket.connect((host, port))
