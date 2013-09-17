# coding=utf-8
import unittest
import os
pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
import modloader
import tempfile

class TestEmptyDir(unittest.TestCase):
    def setUp(self):
        """
            Creates an empty directory with nothing in it.
        """
        self.td = tempfile.mkdtemp()

    def test_unnamed_function(self):
        """
            Empty function name should raise a ValueError.
        """
        with self.assertRaises(ValueError):
            modloader.get_modules(self.td, "")

    def test_no_function(self):
        """
            Missing function name should raise a ValueError.
        """
        with self.assertRaises(ValueError):
            modloader.get_modules(self.td, None)

    def tearDown(self):
        """
            Remove temporary files again.
        """
        os.rmdir(self.td)

if __name__ == '__main__':
    unittest.main()
