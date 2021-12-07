""" Build a python script for the aeon3yw distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

The PyWriter project (see see https://github.com/peter88213/PyWriter)
must be located on the same directory level as the aeon3yw project. 

For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = 'aeon3yw_.pyw'
TARGET_FILE = BUILD + 'aeon3yw.pyw'


def main():
    os.chdir(SRC)

    try:
        os.remove(TARGET_FILE)

    except:
        pass

    inliner.run(SOURCE_FILE, TARGET_FILE, 'pywaeon3', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../../PyWriter/src/')
    print('Done.')


if __name__ == '__main__':
    main()
