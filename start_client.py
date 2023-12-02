"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file instantiates a Client object and starts it.
"""

from client import Client

# Input the host name and port number
host = input("Enter the host name: ")
while True:
    try:
        port = int(input("Enter the port number: "))
        break
    except ValueError:
        print("Invalid port number.")

# Instantiate the client
client = Client(host, port)

# Start the client
pass
