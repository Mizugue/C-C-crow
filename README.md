# C&C-Crow 🐦‍⬛
* Python backdoor within 18 functionalities 

First Contact w/ server
>![backofc](https://github.com/Mizugue/Crow-CC/assets/126506298/2ca35f28-369e-432f-bd90-db8a9b160473)




```
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

```

___

---

>>>FUNCTIONALITIES 🔧
---


    >cd directory
    *Allows you to move to a different directory on the victim's machine.
    ---
    >dir directory
    *Allows you to list the files in a directory on the victim's machine.
    ---
    >exec command timeout(sec)
    *Allows you to execute any command in the console of the victim's machine. The timeout parameter specifies the maximum execution time, after which the command returns the partial output.
    ---
    >screenshot
    *Captures a screenshot of the victim's machine.
    ---
    >get_system_info
    *Returns detailed information about the victim's machine, including platform, CPU, memory, disk, network, and more.
    ---
    >upload filename
    *Uploads a file from the server to the client.
    ---
    >download filename
    *Downloads a file from the client to the server.
    ---
    >web-open url
    *Opens the specified URL on the victim's machine.
    ---
    >pop-up msg
    *Displays a message on the victim's machine.
    ---
    >persist
    *Adds a new key in the system registry to make the client execute every time the system reboots.
    ---
    >lazagne timeout(sec)
    *Downloads and executes LaZagne. If the execution exceeds the specified timeout, it returns the partial output.
    Who is LaZagne? Check here -> LaZagne GitHub
    ---
    >crypter & decrypter
    *Uses the Fernet library for symmetric encryption and decryption of the current directory. It uses AES-128 for encryption and decryption, sends the key to the server, and then self-deletes on the client.
    ---
    >auto_remove
    *The client self-deletes by overwriting data before deletion. The file is filled with a sequence of zeros.
    ---
    >keylogger interval(sec)
    *Activates the keylogger and dumps the captured data at the specified interval.
    ---
    >ask_permission
    *Asks the client for permission to run the script with administrator privileges.
    ---
    >disable_defender
    *Uses PowerShell commands to disable various features of Windows Defender, preventing its monitoring.
    ---
    >grab_cam
    *Captures an image from the webcam of the victim's machine.
    ---
    ---
>[Disclaimer]
>This project is intended for educational purposes only. The backdoor implemented here is designed to demonstrate concepts related to cybersecurity and network programming. Do not use this software for malicious purposes. Unauthorized access to computer systems and data is illegal and unethical.        
