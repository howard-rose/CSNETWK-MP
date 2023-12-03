"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file contains the Client class.
An instance of the Server must be running before any Client can connect.
"""

import socket
from os import mkdir


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
        try:
            mkdir(filepath)
        except FileExistsError:
            pass

        self.filepath = filepath

    def send(self, data):
        """
        This method sends data to the server.
        :param data: The data to send to the server.
        :return: None
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Send the data
        self.connection.send(data)

    def receive(self):
        """
        This method receives data from the server.
        :return: The data received from the server.
        """
        # Check if the client is connected to a server
        if self.connection is None:
            print('Not connected to any server')
            return False

        # Receive the data
        return self.connection.recv(1024)

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
        return self.receive()

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
        file = open(f'{self.filepath}/{filename}', 'rb')

        # Send the file
        self.send(f'STORE {filename} '.encode() + file.read())

        # Close the file
        file.close()

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

        # Open the file
        file = open(f'{self.filepath}/{filename}', 'wb')

        # Receive the file using self.get()
        file.write(self.receive_file(filename))

        # Close the file
        file.close()

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
        return self.receive().decode()
