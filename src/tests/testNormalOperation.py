# coding=utf-8
import unittest
import os
pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
import modloader
import tempfile
import random

MOD_NAMED_FUNC = """
def myfunction(a):
    return a + 1
"""

class TestSingleFunction(unittest.TestCase):
    def setUp(self):
        """
            Create a directory and place a python module in it.
        """
        self.td = tempfile.mkdtemp()
        self.ifile = os.path.join(self.td, "__init__.py")
        self.mfile = os.path.join(self.td, "module.py")
        self.mfilec = os.path.join(self.td, "module.pyc")
        open(self.ifile, 'w').close()
        mf = open(self.mfile, 'w')
        mf.write(MOD_NAMED_FUNC)
        mf.close()

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

    def test_wrong_function(self):
        """
            Wrong function should return empty module list.
        """
        self.assertEqual(modloader.get_modules(self.td, "somefunc"), [])

    def test_success(self):
        """
            Correct function should return a list with one entry (the found
            module) and be able to execute the function and get the expected
            return value.
        """
        mods = modloader.get_modules(self.td, "myfunction")
        self.assertTrue(len(mods) == 1)
        m = mods.pop()
        argument = random.randint(0, 1000)
        value = m.myfunction(argument)
        self.assertEquals(argument + 1, value)

    def tearDown(self):
        """
            Remove temporary files again.
        """
        os.remove(self.ifile)
        os.remove(self.mfile)
        if os.path.exists(self.mfilec):
            os.remove(self.mfilec)
        os.rmdir(self.td)

if __name__ == '__main__':
    unittest.main()
