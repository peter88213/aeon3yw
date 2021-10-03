""" Python unit tests for the aeon3yw project.

Test suite for aeon3yw.pyw.

For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from shutil import copyfile
import os
import unittest
import aeon3yw_


# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/yw7/'

# To be placed in TEST_DATA_PATH:
NORMAL_V3_YW7 = TEST_DATA_PATH + 'normal_v3.yw7'
NORMAL_V3_TL = TEST_DATA_PATH + 'normal_v3.csv'
DATE_LIMITS_YW7 = TEST_DATA_PATH + 'date_limits.yw7'
DATE_LIMITS_TL = TEST_DATA_PATH + 'date_limits.csv'

# Test data
INI_FILE = TEST_EXEC_PATH + 'aeon3yw.ini'
TEST_YW7 = TEST_EXEC_PATH + 'yw7 Sample Project.yw7'
TEST_TL = TEST_EXEC_PATH + 'yw7 Sample Project.csv'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def remove_all_testfiles():

    try:
        os.remove(TEST_YW7)

    except:
        pass

    try:
        os.remove(TEST_TL)
    except:
        pass

    try:
        os.remove(INI_FILE)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):

        try:
            os.mkdir(TEST_EXEC_PATH)

        except:
            pass

        remove_all_testfiles()

    def test_aeon3(self):
        copyfile(NORMAL_V3_TL, TEST_TL)
        os.chdir(TEST_EXEC_PATH)
        aeon3yw_.run(TEST_TL, silentMode=True)
        self.assertEqual(read_file(TEST_YW7), read_file(NORMAL_V3_YW7))

    def test_date_limits(self):
        copyfile(DATE_LIMITS_TL, TEST_TL)
        os.chdir(TEST_EXEC_PATH)
        aeon3yw_.run(TEST_TL, silentMode=True)
        self.assertEqual(read_file(TEST_YW7), read_file(DATE_LIMITS_YW7))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
