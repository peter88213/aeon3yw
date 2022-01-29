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
from pathlib import Path

from pywriter.ui.ui import Ui
from pywriter.ui.ui_tk import UiTk
from pywriter.config.configuration import Configuration

from pywaeon3.pywaeon3_converter import Pywaeon3Converter

SUFFIX = ''
APPNAME = 'aeon3yw'

SETTINGS = dict(
    part_number_prefix='Part',
    chapter_number_prefix='Chapter',
    type_event='Event',
    type_character='Character',
    type_location='Location',
    type_item='Item',
    character_label='Participant',
    location_label='Location',
    item_label='Item',
    part_desc_label='Label',
    chapter_desc_label='Label',
    scene_desc_label='Summary',
    scene_title_label='Label',
    notes_label='Notes',
    tag_label='Tags',
    viewpoint_label='Viewpoint',
    character_bio_label='Summary',
    character_aka_label='Nickname',
    character_desc_label1='Characteristics',
    character_desc_label2='Traits',
    character_desc_label3='',
    location_desc_label='Summary',
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
        sourceDir = f'{sourceDir}/'

    iniFileName = f'{APPNAME}.ini'
    iniFiles = [f'{installDir}{iniFileName}', f'{sourceDir}{iniFileName}']

    configuration = Configuration(SETTINGS)

    for iniFile in iniFiles:
        configuration.read(iniFile)

    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    converter = Pywaeon3Converter()
    converter.ui = ui
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Aeon Timeline 3 to yWriter converter',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the .aeon or .csv file.')

    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()

    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config/'

    except:
        installDir = ''

    run(args.sourcePath, args.silent, installDir)
