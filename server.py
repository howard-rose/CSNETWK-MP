"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file contains the Server class.
An instance of the Server must be running before any Client can connect.
"""

import socket
import threading
import os


class Server:
    """
    This class represents a Server that will accept connections from Clients.
    The purpose of the server is to serve files to clients as well as to
    receive files from clients.

    The server will be able to handle multiple clients at once.
    :param port: The port number to listen to.
    """

    # Store the current connections
    connections = []
    connection = None

    def __init__(self, port, dir_path):
        # Create a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.socket.bind(('', port))

        # Listen for connections
        self.socket.listen(5)

        # Create server directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)
        self.dir_path = dir_path

    def send(self, data):
        self.connection.send(data)

    def receive(self):
        return self.connection.recv(1024)

    def accept(self):
        self.connection, addr = self.socket.accept()
        return self.connection, addr

    def register(self, username):
        pass

    def get(self, filename):
        try:
            with open(f'{self.dir_path}/{filename.decode()}', 'rb') as file:
                self.send(file.read())
        except FileNotFoundError:
            self.send('File not found'.encode())

    def store(self, filename, content):
        with open(f'{self.dir_path}/{filename.decode()}', 'wb') as file:
            file.write(content)

    def dir(self):
        listdir = os.listdir(self.dir_path)
        self.send(('\n'.join(listdir)).encode())