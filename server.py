import socket
import threading   # allows creation of multiple threads within 1 python program
HEADER = 64   # global for max message length
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# better way to do what is being done above so the ip address automatically changes
# this is to get ip address by host name
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# this is to create a websocket af inet is over the internet
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)   # binding server socket to address
def handle_client (conn, addr):
    print(f"new connection {addr}")
    # another infinite whileloop
    connected = True
    while connected:

        # message will be decoded in utf 8 format to string so we know the size of the message
        msg_len = conn.recv(HEADER).decode(FORMAT)   # maximum bytes of 64 and if under 64 messages will be padded
        if msg_len:
            msg_len = int(msg_len) # we convert the same message to an int
            msg = conn.recv(msg_len).decode(FORMAT)   # we convert the message to the string
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False # loop exit when the client sends disconnect message




def start():
    server.listen() # listening for new connections
    print(f"listening on {SERVER}")   # listening on ip address
    while True:
        # infinite loop to continue listening
        # conn is for connection while addr is for address
        conn, addr = server.accept()   # this waits for a new connection to the server essentially why listening happens
        # essentially when there is a new connecton there is another instance of the program which happens
        # the other instance calls the handle client function with conn and addr as the arguments
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # shows the number of threads connected in this program
        # number of threads represents number of clients
        # start thread is always running so there needs to be a subtraction of 1 from the threads
        print(f"active connections {threading.activeCount() - 1}")


print("Server is starting")
start()