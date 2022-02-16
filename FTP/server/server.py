import socket
import os 

# --- program functions --- # 

def list_files():

    print("Showing files")
            
    message = 'root/'
    
    for root, dirs, files in os.walk("./server_data/"):
        level = root.replace("./server_data/", '').count(os.sep)
        indent = ' ' * 4 * (level)
        message = message + f'{indent}{os.path.basename(root)}/\n'
        subindent = ' ' * 4 * (level + 1)
        
        for f in files:
            message = message + '{}{}\n'.format(subindent, f)

    print(message)
    connection.send(message.encode('utf-8'))

def receive():

    print("Downloading file!")

    if connection.recv(1024).decode('utf-8') == "PASS":
        filename = connection.recv(1024).decode('utf-8')
        print("Downloading ", filename)

        file_data = connection.recv(1024).decode('utf-8')

        print(file_data)

        try:
            file = open("./server_data/" + filename, 'w')

            if file_data != "<EMPTY>":
                file.write(file_data)

            file.close()

        except:

            head, tail = os.path.split(filename)
            os.makedirs("./server_data/" + head)

            file = open("./server_data/" + head + "/" + tail, 'w')

            if file_data != "<EMPTY>":
                file.write(file_data)

        print("received ", file_data)

        connection.send("OK".encode('utf-8'))

        print("done")

    else:

        print("Worng Command")

def check_name(filename):

    working = 1

    try:
        file = open("./server_data/" + filename, 'r')

    except:
        working = 0

    return working

def send():

    print("Sending file!")

    filename = connection.recv(1024).decode('utf-8')

    if check_name(filename) == 1:
        connection.send("PASS".encode('utf-8'))
        file = open("./server_data/" + filename, 'r')

        print("./server_data/" + filename)

        file_data = file.read(1024)

        print("SENDING OK")

        connection.send("OK".encode('utf-8'))

        if file_data != "":
            connection.send(file_data.encode('utf-8'))

        else:
            connection.send("<EMPTY>".encode('utf-8'))

        print("TRY")

        #except:
           # connection.send("ERROR".encode('utf-8'))
          #  connection.send(' '.encode('utf-8'))
          #  print("EXCEPT")
    else:
        connection.send("ERROR".encode('utf-8'))
        
def delete():

    print("Removing file")

    filename = connection.recv(1024).decode('utf-8')

    try:
        os.remove("./server_data/" + filename)
        connection.send("file deleted".encode('utf-8'))

    except:
        connection.send("file does not exist".encode('utf-8'))

def close_connection():

    print(f"Closing connection with {address}")
    
    connection.close()

# --- program start --- # 

if __name__ == '__main__':

    soc = socket.socket()
    host = socket.gethostname()
    port = 20200

    soc.bind((host, port))
    soc.listen(1)

    print(f"> Server started!\n> Waiting for incomming connections\n> Note: open a client and connect using '{host}'\n>")
    connection, address = soc.accept()
    print(address, "has connected to the server!\n>")

    # --- program loop --- # 

    while True:
        command = str(connection.recv(1024).decode('utf-8'))

        if command == "LIST":
            list_files()
            continue

        elif command == "UPLOAD":
            receive()
            continue

        elif command == "DOWNLOAD":
            send()
            continue
        
        elif command == "DELETE":
            delete()
            continue
        
        elif command == "EXIT":
            close_connection()
            break

        else:
            pass