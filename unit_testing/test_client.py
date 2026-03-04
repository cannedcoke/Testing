import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validations import validate_message
import unittest

class TestWriteFunction(unittest.TestCase):
    
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
        
        
if __name__ == "__main__":
    unittest.main()