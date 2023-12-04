"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file contains the Client class.
An instance of the Server must be running before any Client can connect.
"""

import socket
from os import makedirs


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
    filepath = None

    def __init__(self, filepath):
        # Create a client directory if it does not exist
        makedirs(filepath, exist_ok=True)

        self.filepath = filepath

    def send(self, data, buff_size=1024):
        """
        This method sends data to the server.
        :param data: The data to send to the server.
        :param buff_size: The size of the buffer to use.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Send the data in chunks
        try:
            for i in range(0, len(data), buff_size):
                self.connection.send(data[i:i + buff_size])
        except ConnectionResetError:
            print('Connection was dead, closing connection')
            self.connection.close()
            self.connection = None
            return

    def receive(self, buff_size=1024):
        """
        This method receives data from the server.
        :param buff_size: The size of the buffer to use.
        :return: The data received from the server.
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Receive the data in buffers
        try:
            buf = self.connection.recv(buff_size)
            while buf:
                yield buf
                if len(buf) < buff_size:
                    break
                buf = self.connection.recv(buff_size)
        except ConnectionResetError:
            print('Server left, closing connection')
            self.connection.close()
            self.connection = None
            return

    def join(self, host, port, blocking=True):
        """
        This method connects the client to the server.
        :param host: The host name of the server to connect to.
        :param port: The port number of the server to connect to.
        :param blocking: Whether the socket should be blocking.
        :return: None
        """
        # Warn if already connected to a server
        if self.connection is not None:
            print('Already connected to a server')
            return False

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(5)
        self.connection.setblocking(blocking)
        # Connect to the server
        self.connection.connect((host, port))

        return True

    def leave(self):
        """
        This method closes the connection to the server.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Close the connection
        self.connection.close()

        # Set the connection to None
        self.connection = None

        return True

    def register(self, username):
        """
        This method registers the client to the server.
        :param username: The username of the client.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Send the username
        self.send(f'REGISTER {username}'.encode())

    def receive_file(self, filename):
        """
        This method requests a file from the server.
        :param filename: The name of the file to request.
        :return: The contents of the file requested.
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Send the request
        self.send(f'GET {filename}'.encode())

        # Receive the response
        res = b''.join(self.receive())

        # Check if the file was found
        if res == b'ERROR: File not found':
            print('File not found')
            return False

        return res

    def store(self, filename):
        """
        This method sends a file to the server.
        :param filename: The name of the file to send.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Open the file in the client directory
        with open(f'{self.filepath}/{filename}', 'rb') as file:
            # Send the file
            self.send(f'STORE {filename} '.encode() + file.read())

        print('File sent')

    def get(self, filename):
        """
        This method receives a file from the server.
        :param filename: The name of the file to receive.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Receive the file using self.receive_file()
        file_bytes = self.receive_file(filename)

        # Open the file
        if file_bytes:
            with open(f'{self.filepath}/{filename}', 'wb') as file:
                file.write(file_bytes)
                print('File received')


    def dir(self):
        """
        This method requests the list of files from the server.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Send the request
        self.send('DIR'.encode())

        # Receive the response
        return b''.join(self.receive()).decode()
