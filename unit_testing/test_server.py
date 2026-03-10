import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch, MagicMock
import threading
import server


class testBroadcast(unittest.TestCase):
    # initial setup to start with clean slate
    def setUp(self):
        server.clients = []
        server.nicks = []
        server.lock = threading.Lock()
        
    # replaces safe send during testing in server
    @patch("server.safe_send")#lets me use mock_safe_send parameter
    def test_safe_send_for_each_client(self, mock_safe_send):
        client1 = MagicMock()
        client2 = MagicMock()
        
        server.clients =[client1, client2]
        
        # la b es para que el mensaje este en forma de bytes  
        message = b"hey"
        
        server.broadcast(message)
        
        self.assertEqual(mock_safe_send.call_count,2)
        mock_safe_send.assert_any_call(client1,message)
        mock_safe_send.assert_any_call(client2,message)


class testSafeSend(unittest.TestCase):
    
    def test_send_success(self):
        client = MagicMock()
        message = b"heyy"
        
        server.safe_send(client,message)
        
        client.send.assert_called_once_with(message)
        
    def test_retry_send(self):
        client = MagicMock()
        message = b"whatever"


        client.send.side_effect = [Exception(),None]
        
        server.safe_send(client,message,retries=3)
        self.assertEqual(client.send.call_count,2)
        
    @patch("server.remove")
    def test_remove_client_on_falure(self,mock_remove):
        client = MagicMock()
        message = b"idk"
        
        client.send.side_effect = Exception()
        
        server.safe_send(client,message,retries=3)
        
        self.assertEqual(client.send.call_count,3)
        mock_remove.assert_called_once_with(client)
        
        
        
if __name__ == "__main__":
    unittest.main()