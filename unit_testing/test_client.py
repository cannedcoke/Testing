import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validations import validate_message, validate_nickname
import unittest

class TestWriteFunction(unittest.TestCase):
    
    
    # CLIENT INPUT VALIDATION TESTS--------
    def test_empty_message(self):
        self.assertFalse(validate_message(""),"empty messages are not allowed")
        
    def test_refuse_only_spaces(self):
        self.assertFalse(validate_message("    "),"spaces only are not allowed")
        
    def test_refuse_long_messages(self):
        self.assertFalse(validate_message("a"*51),"message too long")
        
    def test_valid_message(self):
        self.assertTrue(validate_message("hey"))
        
    def test_valid_message_with_sapces(self):
        self.assertTrue(validate_message("  hey  "))
    
    #CLIENT NICKNAME VALIDATION TESTS
    
    def test_empty_nickname(self):
        self.assertFalse(validate_nickname(""),"empty messages are not allowed")
        
    def test_refuse_only_spaces_in_nick(self):
        self.assertFalse(validate_nickname("    "),"spaces only are not allowed")
        
    def test_refuse_long_nicknames(self):
        self.assertFalse(validate_nickname("a"*11),"message too long")
        
    def test_valid_message(self):
        self.assertTrue(validate_nickname("miki"))
        
    def test_valid_message_with_sapces(self):
        self.assertTrue(validate_nickname("  miki  "))
        
        
if __name__ == "__main__":
    unittest.main()