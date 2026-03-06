import threading 
import socket 
from colorama import init, Fore, Style
init()

HOST = '127.0.0.1'
PORT = 9090 

def start_server(host=HOST, port=PORT):
    global server, clients, nicks, lock

    clients = []
    nicks = []
    lock = threading.Lock()

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    server.settimeout(0.5)
    
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "server is listening... "+ Style.RESET_ALL)
    thread = threading.Thread(target=receive, daemon=True)
    thread.start()

def broadcast(message):
    with lock:
        for client in clients:
            safe_send(client,message)
        
def safe_send(client, message, retries=3):
    for _ in range(retries):
        try:
            client.send(message)
            return
        except:
            continue
    remove(client) 

def remove(client):
    with lock:
            if client not in clients:
                return
            
            index = clients.index(client)
            nick = nicks[index]
            
            try:
                txt = (Fore.RED + Style.BRIGHT + "You left the chat."+ Style.RESET_ALL)
                client.send(txt.encode('utf-8'))
            except:
                pass
            
            clients.remove(client)
            nicks.remove(nick)
            client.close()
            print(Fore.RED + Style.BRIGHT + f"{nick} has left the chat"+ Style.RESET_ALL)
    txt =(Fore.RED + Style.BRIGHT + f"{nick} left </3"+ Style.RESET_ALL)
    broadcast(txt.encode('utf-8'))

def handle(client):
    while True:
        try:
            try:
                message = client.recv(1024)
                
                if not message:
                    remove(client)
                    break
                
            except OSError:
                remove(client)
                break
            text = message.decode('utf-8').strip()
            if text.endswith("/exit"):
                remove(client)
                break
            
            broadcast(message)
        except:
            remove(client)
            break

def receive():
    while True:
        try:
            client, address = server.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        print(Fore.YELLOW + Style.BRIGHT + f"connected with {str(address)}"+ Style.RESET_ALL)
        client.send('NICK'.encode('utf-8'))
        nick = client.recv(1024).decode('utf-8')
        nicks.append(nick)
        clients.append(client)
        
        print(Fore.YELLOW + Style.BRIGHT + f"the nickname of the client is {nick}!"+ Style.RESET_ALL)
        txt =(Fore.YELLOW + Style.BRIGHT + f"{nick} is here... "+ Style.RESET_ALL)
        broadcast(txt.encode('utf-8'))
        txt =(Fore.LIGHTGREEN_EX + Style.BRIGHT + "connected to the server"+ Style.RESET_ALL)
        client.send(txt.encode('utf-8'))
        
        thread = threading.Thread(target=handle,args=(client,), daemon=True)
        thread.start()

def stop_server():
    for client in list(clients):
        try:
            client.close()
        except:
            pass
    clients.clear()
    nicks.clear()
    server.close()

if __name__ == "__main__":
    start_server()
