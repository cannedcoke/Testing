import socket
import threading
from validations import clientMsg, get_nickname

HOST = '127.0.0.1'
PORT = 9092

nickname = get_nickname()

def recive():
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            message = message.decode('utf-8')
            
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("an error ocurred")
            client.close()
            break

def write():
    while True:
        try:
            msg= clientMsg(nickname)
            if msg:
                client.send(msg.encode('utf-8'))
        except:
            break

def start_client(host=HOST, port=PORT):
    global client
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host, port))

    recive_thread = threading.Thread(target=recive)
    recive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

if __name__ == "__main__":
    start_client()
