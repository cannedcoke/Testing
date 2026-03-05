import socket
import threading
from validations import clientMsg,get_nickname


# direccion para el servidor
HOST = '127.0.0.1'
PORT = 9090

# creo el socket del cliente y creo una conexión TCP con el servidor
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

# intenta recibir constantemente datos, maneja errores, manda el nickname si es pedido
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

# constantemente intenta mandar mensajes

def write():
    while True:
        try:
            msg= clientMsg(nickname)
            if msg:
                client.send(msg.encode('utf-8'))
        except:
            break
        
# uso threads para enviar y recibir mensajes al mismo tiempo sin bloquear el programa
recive_thread = threading.Thread(target=recive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()