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

    # JSON[data][items][byId][<uid>]

    ITEM_DESCRIPTION = 'summary'
    ITEM_START_DATE = 'startDate'
    ITEM_DURATION = 'duration'
    ITEM_LABEL = 'label'
    ITEM_TAGS = 'tags'
    ITEM_TYPE = 'type'
    ITEM_ID = 'id'

    # JSON[definitions][types][byId]

    TYPE_EVENT = 'defaultEvent'
    TYPE_CHARACTER = 'defaultPerson'
    TYPE_LOCATION = 'defaultLocation'
    TYPE_NARRATIVE = 'defaultNarrative'

    # JSON[definitions][types][byId][<uid>]

    TYPE_LABEL = 'label'

    # Events assigned to the "narrative" become
    # regular scenes, the others become Notes scenes.

    DATE_LIMIT = (datetime(100, 1, 1) - datetime.min).total_seconds()
    # Dates before 100-01-01 can not be displayed properly in yWriter

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

        # Make sure there is an "AD" era.

        eras = jsonData['definitions']['calendar']['eras']
        adEra = None

        for i in range(len(eras)):

            if eras[i]['name'] == 'AD':
                adEra = i
                break

        #--- Create characters, locations, and items.

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

            if dataItem[self.ITEM_TYPE] == self.TYPE_EVENT:
                #--- Create scenes.

                eventCount += 1
                scId = str(eventCount)
                scIdsByGuid[uid] = scId
                self.scenes[scId] = Scene()
                self.scenes[scId].status = 1
                # Set scene status = "Outline"
                self.scenes[scId].title = dataItem[self.ITEM_LABEL]
                self.scenes[scId].desc = dataItem[self.ITEM_DESCRIPTION]
                timestamp = dataItem[self.ITEM_START_DATE]['timestamp']

                if timestamp is not None and timestamp >= self.DATE_LIMIT:
                    # Restrict date/time calculation to dates within yWriter's range

                    sceneStart = datetime.min + timedelta(seconds=timestamp)
                    startDateTime = sceneStart.isoformat().split('T')
                    self.scenes[scId].date = startDateTime[0]
                    self.scenes[scId].time = startDateTime[1]

            elif dataItem[self.ITEM_TYPE] == self.TYPE_NARRATIVE:
                #--- Create chapters.

                chapterCount += 1
                chId = str(chapterCount)
                chIdsByGuid[uid] = chId
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = dataItem[self.ITEM_LABEL]
                self.chapters[chId].desc = dataItem[self.ITEM_DESCRIPTION]

            elif dataItem[self.ITEM_TYPE] == self.TYPE_CHARACTER:
                #--- Create characters.

                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[uid] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = dataItem[self.ITEM_LABEL]
                self.characters[crId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtCharacters.append(crId)

            elif dataItem[self.ITEM_TYPE] == self.TYPE_LOCATION:

                #--- Create locations.

                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[uid] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[crId].title = dataItem[self.ITEM_LABEL]
                self.locations[crId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtLocations.append(lcId)

            '''
            elif dataItem[self.ITEM_TYPE] == self.TYPE_ITEM:

                #--- Create items.

                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[uid] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = dataItem[self.ITEM_LABEL]
                self.items[itId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtItems.append(itId)
            '''

        #--- Build the narrative structure.

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
                            self.chapters[chIdsByGuid[narrative1['id']]].chLevel = 0

                elif narrative1['id'] in scIdsByGuid:
                    self.chapters[chIdsByGuid[narrative1['id']]].srtScenes.append(scIdsByGuid[narrative1['id']])
                    self.chapters[chIdsByGuid[narrative0['id']]].chLevel = 0

        # Create a dummy chapter, if there is no other structure.

        if self.chapters == {}:
            self.chapters['1'] = Chapter()
            self.chapters['1'].title = 'Chapter 1'
            self.chapters['1'].chType = 0
            self.srtChapters.append('1')

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'
