"""Provide a class for Aeon Timeline 3 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import json
from datetime import datetime
from datetime import timedelta

from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from pywaeon3.aeon3_fop import scan_file


class JsonTimeline3(Novel):
    """File representation of an Aeon Timeline 3 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeon'
    DESCRIPTION = 'Aeon Timeline 3 project'
    SUFFIX = ''

    DATE_LIMIT = (datetime(100, 1, 1) - datetime.min).total_seconds()
    # Dates before 100-01-01 can not be displayed properly in yWriter

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        Novel.__init__(self, filePath, **kwargs)

        # JSON[definitions][types][byId]

        self.LABEL_EVENT = kwargs['label_event']
        self.LABEL_CHARACTER = kwargs['label_character']
        self.LABEL_LOCATION = kwargs['label_location']
        self.LABEL_ITEM = kwargs['label_item']

        # Misc.

        self.partHdPrefix = kwargs['part_heading_prefix']
        self.chapterHdPrefix = kwargs['chapter_heading_prefix']

    def read(self):
        """Extract the JSON part of the Aeon Timeline 3 file located at filePath, 
        fetching the relevant data.
        Extend the superclass.

        Return a message beginning with SUCCESS or ERROR.
        """

        jsonPart = scan_file(self.filePath)

        if not jsonPart:
            return 'ERROR: No JSON part found.'

        elif jsonPart.startswith('ERROR'):
            return jsonPart

        try:
            jsonData = json.loads(jsonPart)

        except('JSONDecodeError'):
            return 'ERROR: Invalid JSON data.'

        #--- Find types.

        typeEvent = None
        typeCharacter = None
        typeLocation = None
        typeItem = None
        NarrativeFolderTypes = []

        for uid in jsonData['definitions']['types']['byId']:

            if jsonData['definitions']['types']['byId'][uid]['isNarrativeFolder']:
                NarrativeFolderTypes.append(uid)

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self.LABEL_EVENT:
                typeEvent = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self.LABEL_CHARACTER:
                typeCharacter = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self.LABEL_LOCATION:
                typeLocation = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self.LABEL_ITEM:
                typeItem = uid

        #--- Read items.

        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        scIdsByGuid = {}
        chIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0
        eventCount = 0
        chapterCount = 0

        for uid in jsonData['data']['items']['byId']:
            dataItem = jsonData['data']['items']['byId'][uid]

            if dataItem['type'] == typeEvent:

                #--- Create scenes.

                eventCount += 1
                scId = str(eventCount)
                scIdsByGuid[uid] = scId
                self.scenes[scId] = Scene()
                self.scenes[scId].status = 1
                # Set scene status = "Outline"
                self.scenes[scId].isNotesScene = True
                # Will be set to False later if it is part of the narrative.
                self.scenes[scId].title = dataItem['label']
                self.scenes[scId].desc = dataItem['summary']
                timestamp = dataItem['startDate']['timestamp']

                #--- Get scene tags

                for tagId in dataItem['tags']:

                    if self.scenes[scId].tags is None:
                        self.scenes[scId].tags = []

                    self.scenes[scId].tags.append(jsonData['data']['tags'][tagId])

                #--- Get scene date, time, and duration.

                if timestamp is not None and timestamp >= self.DATE_LIMIT:
                    # Restrict date/time calculation to dates within yWriter's range

                    sceneStart = datetime.min + timedelta(seconds=timestamp)
                    startDateTime = sceneStart.isoformat().split('T')
                    self.scenes[scId].date = startDateTime[0]
                    self.scenes[scId].time = startDateTime[1]

                    # Calculate duration

                    if dataItem['duration']['years'] > 0 or dataItem['duration']['months'] > 0:
                        endYear = sceneStart.year + dataItem['duration']['years']
                        endMonth = sceneStart.month

                        if dataItem['duration']['months'] > 0:
                            endYear += dataItem['duration']['months'] // 12
                            endMonth += dataItem['duration']['months']

                            while endMonth > 12:
                                endMonth -= 12

                        sceneDuration = datetime(endYear, endMonth, sceneStart.day) - \
                            datetime(sceneStart.year, sceneStart.month, sceneStart.day)
                        lastsDays = sceneDuration.days
                        lastsHours = sceneDuration.seconds // 3600
                        lastsMinutes = (sceneDuration.seconds % 3600) // 60

                    else:
                        lastsDays = 0
                        lastsHours = 0
                        lastsMinutes = 0

                    lastsDays += dataItem['duration']['weeks'] * 7
                    lastsDays += dataItem['duration']['days']
                    lastsDays += dataItem['duration']['hours'] // 24
                    lastsHours += dataItem['duration']['hours'] % 24
                    lastsHours += dataItem['duration']['minutes'] // 60
                    lastsMinutes += dataItem['duration']['minutes'] % 60
                    lastsMinutes += dataItem['duration']['seconds'] // 60
                    lastsHours += lastsMinutes // 60
                    lastsMinutes %= 60
                    lastsDays += lastsHours // 24
                    lastsHours %= 24
                    self.scenes[scId].lastsDays = str(lastsDays)
                    self.scenes[scId].lastsHours = str(lastsHours)
                    self.scenes[scId].lastsMinutes = str(lastsMinutes)

            elif dataItem['type'] in NarrativeFolderTypes:

                #--- Create chapters.

                chapterCount += 1
                chId = str(chapterCount)
                chIdsByGuid[uid] = chId
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = dataItem['label']
                self.chapters[chId].desc = dataItem['summary']

            elif dataItem['type'] == typeCharacter:

                #--- Create characters.

                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[uid] = crId
                self.characters[crId] = Character()

                if dataItem['shortLabel']:
                    self.characters[crId].title = dataItem['shortLabel']

                else:
                    self.characters[crId].title = dataItem['label']

                self.characters[crId].fullName = dataItem['label']
                self.characters[crId].desc = dataItem['summary']
                self.srtCharacters.append(crId)

                #--- Get character tags.

                for tagId in dataItem['tags']:

                    if self.characters[crId].tags is None:
                        self.characters[crId].tags = []

                    self.characters[crId].tags.append(jsonData['data']['tags'][tagId])

            elif dataItem['type'] == typeLocation:

                #--- Create locations.

                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[uid] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[crId].title = dataItem['label']
                self.locations[crId].desc = dataItem['summary']
                self.srtLocations.append(lcId)

                #--- Get location tags.

                for tagId in dataItem['tags']:

                    if self.locations[lcId].tags is None:
                        self.locations[lcId].tags = []

                    self.locations[lcId].tags.append(jsonData['data']['tags'][tagId])

            elif dataItem['type'] == typeItem:

                #--- Create items.

                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[uid] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = dataItem['label']
                self.items[itId].desc = dataItem['summary']
                self.srtItems.append(itId)

                #--- Get item tags.

                for tagId in dataItem['tags']:

                    if self.items[itId].tags is None:
                        self.items[itId].tags = []

                    self.items[itId].tags.append(jsonData['data']['tags'][tagId])

        #--- Build a narrative structure with 2 or 3 levels.

        for narrative0 in jsonData['data']['narrative']['children']:

            if narrative0['id'] in chIdsByGuid:
                self.srtChapters.append(chIdsByGuid[narrative0['id']])

            for narrative1 in narrative0['children']:

                if narrative1['id'] in chIdsByGuid:
                    self.srtChapters.append(chIdsByGuid[narrative1['id']])
                    self.chapters[chIdsByGuid[narrative0['id']]].chLevel = 1

                    for narrative2 in narrative1['children']:

                        if narrative2['id'] in scIdsByGuid:
                            self.chapters[chIdsByGuid[narrative1['id']]].srtScenes.append(
                                scIdsByGuid[narrative2['id']])
                            self.scenes[scIdsByGuid[narrative2['id']]].isNotesScene = False
                            self.chapters[chIdsByGuid[narrative1['id']]].chLevel = 0

                elif narrative1['id'] in scIdsByGuid:
                    self.chapters[chIdsByGuid[narrative0['id']]].srtScenes.append(scIdsByGuid[narrative1['id']])
                    self.scenes[scIdsByGuid[narrative1['id']]].isNotesScene = False
                    self.chapters[chIdsByGuid[narrative0['id']]].chLevel = 0

        #--- Auto-number untitled chapters.

        partCount = 0
        chapterCount = 0

        for chId in self.srtChapters:

            if self.chapters[chId].chLevel == 1:
                partCount += 1

                if not self.chapters[chId].title:
                    self.chapters[chId].title = self.partHdPrefix + ' ' + str(partCount)

            else:
                chapterCount += 1

                if not self.chapters[chId].title:
                    self.chapters[chId].title = self.chapterHdPrefix + ' ' + str(chapterCount)

        #--- Create a dummy chapter, if there is no other structure.
        # This is because yWriter needs at least one chapter.

        if self.chapters == {}:
            self.chapters['1'] = Chapter()
            self.chapters['1'].title = self.chapterHdPrefix + ' 1'
            self.chapters['1'].chType = 0
            self.srtChapters.append('1')

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'
