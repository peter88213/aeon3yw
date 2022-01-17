"""Provide an Aeon3 converter class for yWriter projects. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ff import YwCnvFf
from pywriter.converter.new_project_factory import NewProjectFactory

from pywaeon3.json_timeline3 import JsonTimeline3
from pywaeon3.csv_timeline3 import CsvTimeline3


class Pywaeon3Converter(YwCnvFf):
    """A converter class for JSON timeline import."""
    CREATE_SOURCE_CLASSES = [JsonTimeline3, CsvTimeline3]

    def __init__(self):
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
