"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file instantiates a Server object and starts it.
"""

from server import Server


def handle_request(req_string):
    # Server must handle the ff. request strings:
    # REGISTER {username}
    # GET {filename}
    # STORE {filename} {content}
    # DIR

    req_list = req_string.split()
    req, args = (req_list[0].decode(), [req_list[1].decode(), b' '.join(req_list[2:])]
                if len(req_list) > 2 else [req_list[1].decode()] if len(req_list) == 2 else [])

    print('=====')
    print('Received request:', req, args)

    match req, args:
        case 'REGISTER', [username]:
            server.register(username)
        case 'GET', [filename]:
            server.get(filename)
        case 'STORE', [filename, content]:
            server.store(filename, content)
        case 'DIR', []:
            server.dir()
        case _:
            print('Invalid request')
            server.send('ERROR: Invalid request'.encode())


# Input the port number
while True:
    try:
        port = int(input('Enter the port number: '))
        break
    except ValueError:
        print('Invalid port number.')

# Instantiate the server
server = Server(port, dir_path='server_directory')

# Start the server
if __name__ == '__main__':
    while True:
        server.accept()
        while True:
            req = b''.join(server.receive())
            if req == b'':
                print('Client left, closing connection')
                server.connection.close()
                break
            handle_request(req)
