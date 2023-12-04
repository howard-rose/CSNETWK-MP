"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file contains the Server class.
An instance of the Server must be running before any Client can connect.
"""

import socket
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
    connections = {}

    def __init__(self, port, dir_path):
        # Create a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.socket.bind(('', port))

        # Listen for connections
        self.socket.listen(5)
        print(f'Listening on port {port}')

        # Create server directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)
        self.dir_path = dir_path

    def send(self, conn, data, buff_size=1024):
        try:
            for i in range(0, len(data), buff_size):
                conn.send(data[i:i + buff_size])
        except ConnectionResetError:
            print('Connection was dead, closing connection')
            conn.close()
            return

    def receive(self, conn, buff_size=1024):
        try:
            buf = conn.recv(buff_size)
            while buf:
                yield buf
                if len(buf) < buff_size:
                    break
                buf = conn.recv(buff_size)
        except ConnectionResetError:
            conn.close()
            return

    def accept(self):
        conn, addr = self.socket.accept()
        self.connections[addr] = conn
        print(f'Connection from {addr}')
        return addr

    def register(self, username):
        pass

    def get(self, filename):
        try:
            with open(f'{self.dir_path}/{filename}', 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return 'ERROR: File not found'.encode()

    def store(self, filename, content):
        # TODO: Catch possible errors?
        with open(f'{self.dir_path}/{filename}', 'wb') as file:
            file.write(content)

    def dir(self):
        listdir = os.listdir(self.dir_path)
        return ('\n'.join(listdir)).encode()