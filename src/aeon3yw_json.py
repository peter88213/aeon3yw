#!/usr/bin/env python3
"""Aeon Timeline 3 to yWriter converter 

Version @release
Requires Python 3.7 or above

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import argparse

from pywriter.ui.ui import Ui
from pywriter.ui.ui_tk import UiTk
from pywriter.config.configuration import Configuration

from pywaeon3.json_converter import JsonConverter

SUFFIX = ''
APPNAME = 'aeon3yw'

SETTINGS = dict(
    part_heading_prefix='Part',
    chapter_heading_prefix='Chapter',
    label_event_type='Event',
    label_character_type='Character',
    label_location_type='Location',
    label_item_type='Item',
    label_participant_ref='Participant',
    label_location_ref='Location',
)


def run(sourcePath, silentMode=True, installDir=''):

    if silentMode:
        ui = Ui('')

    else:
        ui = UiTk('Aeon Timeline 3 to yWriter converter @release')

    #--- Try to get persistent configuration data

    sourceDir = os.path.dirname(sourcePath)

    if sourceDir == '':
        sourceDir = './'

    else:
        sourceDir += '/'

    iniFileName = APPNAME + '.ini'
    iniFiles = [installDir + iniFileName, sourceDir + iniFileName]

    configuration = Configuration(SETTINGS)

    for iniFile in iniFiles:
        configuration.read(iniFile)

    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    converter = JsonConverter()
    converter.ui = ui
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Aeon Timeline 3 to yWriter converter',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the .aeon file.')

    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()
    installDir = os.getenv('APPDATA').replace('\\', '/') + '/pyWriter/' + APPNAME + '/config/'
    run(args.sourcePath, args.silent, installDir)
