import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import socket 
import threading
import time
import pytest
import server

HOST = "127.0.0.1"
TEST_PORT = 9191 #diffrente port for testing
TIMEOUT = 3
 
def connect(nickname, port=TEST_PORT):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    sock.connect((HOST,port))
    assert sock.recv(1024).decode() == 'NICK'
    sock.send(nickname.encode())
    sock.recv(1024)
    # welcome_message = sock.recv(1024).decode()
    # assert 'connected' in welcome_message.lower()
    return sock

def receive_text(sock):
    sock.settimeout(TIMEOUT)
    return sock.recv(1024).decode('utf-8')


@pytest.fixture
def chat_server():
    thread=threading.Thread(target=server.start_server,args=(HOST,TEST_PORT),daemon=True)
    thread.start()
    time.sleep(0.1)
    yield
    server.stop_server()
    time.sleep(0.1)
    

class TestConnection:
    def test_one_client_connects(self,chat_server):
        sock = connect("miki")
        sock.close()
        
    def test_multiple_client_connects(self,chat_server):
        socks = [connect(f"client{i}") for i in range(3)]
        time.sleep(0.5)
        assert len(server.nicks) == 3
        for client in socks:
            client.close()
            
    def test_server_tracks_nicknames(self,chat_server):
        sock = connect("cyanide")
        time.sleep(0.5)
        assert "cyanide" in server.nicks 
        sock.close()
        

class TestMessages:
    def test_message_broadcasted_to_all(self,chat_server):
        client1= connect("client1")
        client2= connect("client2")
        try:
            client1.recv(1024)
        except socket.timeout:
            pass
        
        client2.send("i'm testting".encode())
        time.sleep(0.1)
        assert "i'm testting" in receive_text(client1)
        client1.close()
        client2.close()
        
    def  test_multiple_messages_in_a_row(self,chat_server):
        client1 = connect("client1")
        client2 = connect("client2")
        
        try:
            client1.recv(1024)
        except socket.timeout:
            pass
            
        messages = ["one","two","three"]
        
        for message in messages:
            client2.send(message.encode())
            time.sleep(0.1)
        
        received = []
        
        for _ in messages:
            try:
                received.append(receive_text(client1))
            except socket.timeout:
                break
        
        for message in messages:
            assert any(message in r for r in received)
        client1.close()
        client2.close()
                        
            
        
class TestDisconnets:
    def test_client_removed_on_exit(slef,chat_server):
        client = connect("client")
        time.sleep(0.1)
        assert "client" in server.nicks
        
        client.send("/exit".encode())
        time.sleep(0.1)
        assert "client" not in server.nicks
        client.close()
        
    def test_other_clients_notified_on_leave(self, chat_server):
        client1 = connect("client1") 
        client2 = connect("client2")
        try:
            client1.recv(1024)
        except socket.timeout:
            pass
        client2.send("/exit".encode())
        time.sleep(0.2)
        message = receive_text(client1)
        
        assert "left" in message.lower() or "client2" in message
        client1.close()
         
    def test_handles_abrupt_disconnect(self,chat_server):
        client1 = connect("client1")
        time.sleep(0.1)
        client1.close()
        time.sleep(0.2)
        assert "client1" not in server.nicks
        
    def test_other_clients_not_affected_by_abrupt_disconnect(self,chat_server):
        client1 = connect("client1")
        client2 = connect("client2")
        client3 = connect("client3")
        
        for sock in (client1,client2):
            try:
                sock.recv(1024)
                sock.recv(1024)
            except:
                pass
        client3.close()
        time.sleep(0.2)
        
        for sock in (client1,client2):
            try:
                sock.recv(1024)
            except socket.timeout:
                pass
        
        client1.send("still here".encode())
        time.sleep(0.1)
        assert "still here" in receive_text(client2)
        
        client1.close()
        client2.close()
                 