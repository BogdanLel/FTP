import socket
import os

# --- program functions --- # 

def list_files():

    soc.send('LIST'.encode('utf-8'))
    message = soc.recv(1024).decode('utf-8')
    print("\n\n> The files that exist on the server are:\n")
    print(message)
    waiting = input("\nPress Enter to continue...")

def check_name(filename):

    working = 1

    try:
        file = open("./client_data/" + filename, 'r')

    except:
        working = 0

    return working

def upload():
    soc.send('UPLOAD'.encode('utf-8'))

    filename = input("\t\tSYSTEM> Please enter the path and extension of the file:\n\t\tUSER> ")
    
    if check_name(filename) == 1:
        soc.send("PASS".encode('utf-8'))
        file = open("./client_data/" + filename, 'r')
        file_data = file.read(1024)

        print("\t\tSYSTEM> Sending '" + filename + "'")

        soc.send(filename.encode('utf-8'))

        if file_data != "":
            soc.send(file_data.encode('utf-8'))

        else:
            soc.send("<EMPTY>".encode('utf-8'))

        if soc.recv(1024).decode('utf-8') == "OK":
            print("\t\tSYSTEM> ", filename, "has been sent!")

        else:
            print("\t[ERROR]> There was an issue sending ", filename)

    else:
        print("\t[ERROR]This path/file doesn't exist!")

        soc.send("ERROR".encode('utf-8'))

    waiting = input("\nPress Enter to continue...")

def download():
    soc.send('DOWNLOAD'.encode('utf-8'))
    
    filename = input("\t\t\tSYSTEM> Please enter the path and extension of the file:\n\t\tUSER> ")
    soc.send(filename.encode('utf-8'))

    received = soc.recv(1024).decode('utf-8')

    if received == "PASS":

        if soc.recv(1024).decode('utf-8') == "OK":

            print("\t\tSYSTEM> ", filename, "has been received!")

            file_data = soc.recv(1024).decode('utf-8')

            try:
                file = open("./client_data/" + filename, 'w')
                file.write(file_data)

                file.close()

            except:
                head, tail = os.path.split(filename)
                os.makedirs("./client_data/" + head)
                file = open("./client_data/" + head + "/" + tail, 'w')

                if file_data != "<EMPTY>":
                    file.write(file_data)

                file.close()
                
        else:
            print("SYSTEM> There was an issue receiving ", filename, "\nSYSTEM> The file might not exist.\nSYSTEM> The path might be wrong, use <list>\nSYSTEM> The extension might be wrong")
    
    else:
        print("File doesn't exist on the server!")

    waiting = input("\nPress Enter to continue...")
    
def delete():
    soc.send('DELETE'.encode('utf-8'))
    filename = input("\t\tSYSTEM> Please enter the path and extension of the file:\n\t\t> ")
    soc.send(filename.encode('utf-8'))

    print("> ", soc.recv(1024).decode('utf-8'))

    waiting = input("\nPress Enter to continue...")

def close_program():

    print("Closing connection...")

    soc.send("EXIT".encode('utf-8'))
    soc.close()
    
    print("Closing program...")

# --- program start --- # 

if __name__ == '__main__':

    soc = socket.socket()
    print("\n=============================================================")
    host = input(str("SYSTEM> Please enter the address of the server: "))
    port = 20200

    soc.connect((host, port))
    print(f"SYSTEM> Connected with {host}!")

    # --- program loop --- # 

    while True:
        
        print("\n\nSYSTEM> Please choose a command:")
        command = str(input(" - list / ls\n - download / dl\n - upload / up\n - delete / del\n - exit / x\n\t\tUSER> "))
        
        if command == "list" or command == "ls":
            list_files()
            continue

        if command == "download" or command == "dl":
            download()
            continue

        elif command == "upload" or command == "up":
            upload()
        
        elif command == "delete" or command == "del":
            delete()
        
        elif command == "exit" or command == "x":
            close_program()
            break

        else:
            print("Command unrecognized!")
            pass