"""Provide a generic class for html file import.

Other html file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html.parser import HTMLParser
from pywriter.pywriter_globals import ERROR
from pywriter.model.novel import Novel
from pywriter.html.html_fop import read_html_file


class HtmlFile(Novel, HTMLParser):
    """Generic HTML file representation.
    
    Public methods:
        handle_starttag -- identify scenes and chapters.
        handle comment --
        read --
    """
    EXTENSION = '.html'
    _COMMENT_START = '/*'
    _COMMENT_END = '*/'
    _SC_TITLE_BRACKET = '~'
    _BULLET = '-'
    _INDENT = '>'

    def __init__(self, filePath, **kwargs):
        """Initialize the HTML parser and local instance variables for parsing.
        
        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        The HTML parser works like a state machine. 
        Scene ID, chapter ID and processed lines must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._scId = None
        self._chId = None

    def _convert_to_yw(self, text):
        """Convert html formatting tags to yWriter 7 raw markup.
        
        Positional arguments:
            text -- string to convert.
        
        Return a yw7 markup string.
        Overrides the superclass method.
        """

        #--- Clean up polluted HTML code.
        text = re.sub('</*font.*?>', '', text)
        text = re.sub('</*span.*?>', '', text)
        text = re.sub('</*FONT.*?>', '', text)
        text = re.sub('</*SPAN.*?>', '', text)

        #--- Put everything in one line.
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        while '  ' in text:
            text = text.replace('  ', ' ').strip()

        #--- Replace HTML tags by yWriter markup.
        text = text.replace('<i>', '[i]')
        text = text.replace('<I>', '[i]')
        text = text.replace('</i>', '[/i]')
        text = text.replace('</I>', '[/i]')
        text = text.replace('</em>', '[/i]')
        text = text.replace('</EM>', '[/i]')
        text = text.replace('<b>', '[b]')
        text = text.replace('<B>', '[b]')
        text = text.replace('</b>', '[/b]')
        text = text.replace('</B>', '[/b]')
        text = text.replace('</strong>', '[/b]')
        text = text.replace('</STRONG>', '[/b]')
        text = re.sub('<em.*?>', '[i]', text)
        text = re.sub('<EM.*?>', '[i]', text)
        text = re.sub('<strong.*?>', '[b]', text)
        text = re.sub('<STRONG.*?>', '[b]', text)

        #--- Remove orphaned tags.
        text = text.replace('[/b][b]', '')
        text = text.replace('[/i][i]', '')
        text = text.replace('[/b][b]', '')
        return text

    def _preprocess(self, text):
        """Clean up the HTML code and strip yWriter 7 raw markup.
        
        Positional arguments:
            text -- str: HTML text to be processed.
        
        This prevents accidentally applied formatting from being transferred to the yWriter metadata.
        If rich text is applicable, such as in scenes, overwrite this method in a subclass.
        Return a string.
        """
        text = self._convert_to_yw(text)

        #--- Remove misplaced formatting tags.
        text = re.sub('\[\/*[b|i]\]', '', text)
        return text

    def _postprocess(self):
        """Process the plain text after parsing.
        
        This is a hook for subclasses.
        """

    def handle_starttag(self, tag, attrs):
        """Identify scenes and chapters.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides HTMLparser.handle_starttag() called by the parser to handle the start of a tag. 
        This method is applicable to HTML files that are divided into chapters and scenes. 
        For differently structured HTML files  do override this method in a subclass.
        """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('ScID'):
                    self._scId = re.search('[0-9]+', attrs[0][1]).group()
                    self.scenes[self._scId] = self.SCENE_CLASS()
                    self.chapters[self._chId].srtScenes.append(self._scId)
                elif attrs[0][1].startswith('ChID'):
                    self._chId = re.search('[0-9]+', attrs[0][1]).group()
                    self.chapters[self._chId] = self.CHAPTER_CLASS()
                    self.chapters[self._chId].srtScenes = []
                    self.srtChapters.append(self._chId)

    def handle_comment(self, data):
        """Process inline comments within scene content.
        
        Positional arguments:
            data -- str: comment text. 
        
        Overrides HTMLparser.handle_comment() called by the parser when a comment is encountered.
        """
        if self._scId is not None:
            self._lines.append(f'{self._COMMENT_START}{data}{self._COMMENT_END}')

    def read(self):
        """Parse the file and get the instance variables.
        
        Return a message beginning with the ERROR constant in case of error.
        This is a template method for subclasses tailored to the 
        content of the respective HTML file.
        """
        message, content = read_html_file(self._filePath)
        if message.startswith(ERROR):
            return message

        content = self._preprocess(content)
        self.feed(content)
        self._postprocess()
        return 'Created novel structure from HTML data.'
