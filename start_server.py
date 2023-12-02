"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file instantiates a Server object and starts it.
"""

from server import Server

# Input the port number
while True:
    try:
        port = int(input("Enter the port number: "))
        break
    except ValueError:
        print("Invalid port number.")

# Instantiate the server
server = Server(port)

# Start the server
pass
