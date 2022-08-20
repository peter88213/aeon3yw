"""Provide a class for html outline import.

Conventions:
An outline has at least one third level heading.

-   Heading 1 -- New chapter title (beginning a new section).
-   Heading 2 -- New chapter title.
-   Heading 3 -- New scene title.
-   All other text is considered to be chapter/scene description.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_file import HtmlFile


class HtmlOutline(HtmlFile):
    """HTML outline file representation.

    Import an outline without chapter and scene tags.
    """
    DESCRIPTION = 'Novel outline'
    SUFFIX = ''

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        The HTML parser works like a state machine. 
        Chapter and scene count must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._chCount = 0
        self._scCount = 0

    def handle_starttag(self, tag, attrs):

        if tag in ('h1', 'h2'):
            self._scId = None
            self._lines = []
            self._chCount += 1
            self._chId = str(self._chCount)
            self.chapters[self._chId] = self.CHAPTER_CLASS()
            self.chapters[self._chId].srtScenes = []
            self.srtChapters.append(self._chId)
            self.chapters[self._chId].oldType = '0'
            self.chapters[self._chId].chType = '0'
            if tag == 'h1':
                self.chapters[self._chId].chLevel = 1
            else:
                self.chapters[self._chId].chLevel = 0
        elif tag == 'h3':
            self._lines = []
            self._scCount += 1
            self._scId = str(self._scCount)
            self.scenes[self._scId] = self.SCENE_CLASS()
            self.chapters[self._chId].srtScenes.append(self._scId)
            self.scenes[self._scId].sceneContent = ''
            self.scenes[self._scId].status = self.SCENE_CLASS.STATUS.index('Outline')
        elif tag == 'div':
            self._scId = None
            self._chId = None
        elif tag == 'meta':
            if attrs[0][1].lower() == 'author':
                self.authorName = attrs[1][1]
            if attrs[0][1].lower() == 'description':
                self.desc = attrs[1][1]
        elif tag == 'title':
            self._lines = []

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.

        Overrides HTMLparser.handle_endtag() called by the HTML parser to handle the end tag of an element.
        """
        if tag == 'p':
            self._lines.append('\n')
            if self._scId is not None:
                self.scenes[self._scId].desc = ''.join(self._lines)
            elif self._chId is not None:
                self.chapters[self._chId].desc = ''.join(self._lines)
        elif tag in ('h1', 'h2'):
            self.chapters[self._chId].title = ''.join(self._lines)
            self._lines = []
        elif tag == 'h3':
            self.scenes[self._scId].title = ''.join(self._lines)
            self._lines = []
        elif tag == 'title':
            self.title = ''.join(self._lines)

    def handle_data(self, data):
        """Collect data within scene sections.

        Positional arguments:
            data -- str: text to be stored. 
        
        Overrides HTMLparser.handle_data() called by the parser to process arbitrary data.
        """
        self._lines.append(data.strip())
