"""Provide an Aeon3 converter class for yWriter projects. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ff import YwCnvFf
from aeon3ywlib.new_project_factory import NewProjectFactory
from aeon3ywlib.json_timeline3 import JsonTimeline3
from aeon3ywlib.csv_timeline3 import CsvTimeline3


class Pywaeon3Converter(YwCnvFf):
    """A converter for yWriter project generation from Aeon Timeline 3.

    Overrides the superclass constant CREATE_SOURCE_CLASSES.
    """
    CREATE_SOURCE_CLASSES = [JsonTimeline3, CsvTimeline3]

    def __init__(self):
        """Create a strategy class instance.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
