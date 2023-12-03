"""
Joshua Permito
Philip Anthon Santiago

CSNETWK S12

This file instantiates a Client object and starts command input handling.
"""
from socket import gaierror
from client import Client

# Define command usages
usages = {
    '?': '?',
    'join': 'join <host> <port>',
    'leave': 'leave',
    'register': 'register <handle>',
    'store': 'store <filename>',
    'get': 'get <filename>',
    'exit': 'exit',
    'dir': 'dir'
}

# Instantiate the client
client = Client(filepath='client_directory')


# Implement running commands
def run_command(command, args):
    """
    This method runs a command.
    :param command: The command to run.
    :param args: The arguments to pass to the command.
    :return: None
    """
    # Handle the command
    if command == '?':
        # Print usage message
        print('Usage: /<command> <args>')
        for command, usage in usages.items():
            print('{}: /{}'.format(command, usage))
    elif command == 'join':
        # Check if the number of arguments is correct
        if len(args) != 2:
            print(f'Usage: {usages[command]}')
            return

        # Attempt to connect to the server
        try:
            result = client.join(args[0], int(args[1]), blocking=True)
            if not result:
                return

            # Print success message with host and port
            print('Connected to {} on port {}'.format(args[0], args[1]))
        except ConnectionRefusedError:
            print('Connection refused')
            client.connection = None
        except TimeoutError:
            print('Connection timed out')
            client.connection = None
        except gaierror:
            print('Invalid host')
            client.connection = None
    elif command == 'leave':
        result = client.leave()
        if not result:
            return

        # Print success message
        print('Disconnected from server')
    elif command == 'register':
        # Check if the number of arguments is correct
        if len(args) != 1:
            print(f'Usage: {usages[command]}')
            return

        # Attempt to register the client
        try:
            client.register(args[0])
        except TypeError:
            print('Invalid handle')
    elif command == 'store':
        # Check if the number of arguments is correct
        if len(args) != 1:
            print(f'Usage: {usages[command]}')
            return

        # Attempt to send the file
        try:
            client.store(args[0])
        except FileNotFoundError:
            print('File not found')
    elif command == 'get':
        # Check if the number of arguments is correct
        if len(args) != 1:
            print(f'Usage: {usages[command]}')
            return

        # Attempt to receive the file
        try:
            client.get(args[0])
        except FileNotFoundError:
            print('File not found')
    elif command == 'dir':
        # Attempt to receive the file
        try:
            client.dir()
        except FileNotFoundError:
            print('File not found')
    else:
        print('Invalid command')


def main():
    """
    This method handles user input.
    :return: None
    """
    # Loop forever
    while True:
        # Retrieve full string command from user
        command = input('>>> ')

        # Skip if command does not start with a slash
        if command[0] != '/':
            # Print usage message
            print('Usage: /<command> <args>')
            continue

        # Remove the slash from the command
        command = command[1:]

        # Split the command into a list of arguments, result must be a
        # two-tuple (command, args). Use regex for whitespace splitting.
        args = command.split()
        command = args[0]
        args = args[1:]

        # Break if the command is 'exit'
        if command == 'exit':
            print('Exiting...')
            break

        # Run the command
        run_command(command, args)


if __name__ == '__main__':
    # Start command handler that will handle user input
    main()
