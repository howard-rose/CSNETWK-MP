"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file instantiates a Server object and starts it.
"""

from server import Server
import threading


def handle_request(addr, req_string):
    # Server must handle the ff. request strings:
    # REGISTER {username}
    # GET {filename}
    # STORE {filename} {content}
    # DIR

    req_list = req_string.split()
    req, args = (req_list[0].decode(), [req_list[1].decode(), b' '.join(req_list[2:])]
                if len(req_list) > 2 else [req_list[1].decode()] if len(req_list) == 2 else [])

    print('=====')
    print(f'Received request from {addr}: {req} {args}')

    match req, args:
        case 'REGISTER', [username]:
            res = server.register(username)
            server.send(server.connections[addr], res)
        case 'GET', [filename]:
            res = server.get(filename)
            server.send(server.connections[addr], res)
        case 'STORE', [filename]:
            # TODO: Maybe send response to server?
            content = b''.join(server.receive(server.connections[addr]))
            server.store(filename, content)
        case 'DIR', []:
            res = server.dir()
            server.send(server.connections[addr], res)
        case _:
            print('Invalid request')
            server.send('ERROR: Invalid request'.encode())


def handle_client(addr):
    while True:
        req = b''.join(server.receive(server.connections[addr]))
        if req == b'':
            print(f'Client {addr} left, closing connection')
            server.connections[addr].close()
            break
        handle_request(addr, req)


if __name__ == '__main__':
    # Input the port number
    while True:
        try:
            port = int(input('Enter the port number: '))
            break
        except ValueError:
            print('Invalid port number.')

    # Instantiate the server
    server = Server(port, dir_path='server_directory')

    # Track all threads
    threads = []

    try:
        while True:
            # Accept client connections
            addr = server.accept()

            # Start new thread
            t = threading.Thread(target=handle_client, args=(addr,))
            t.start()

            threads.append(t)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        # TODO: Close all client connections
        for t in threads:
            t.join()
