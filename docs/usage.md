[Project homepage](https://peter88213.github.io/aeon3yw)

------------------------------------------------------------------

The aeon3yw Python script creates a yWriter 7 project from a csv file exported by Aeon Timeline 3.

## Instructions for use

### Intended usage

The included installation script prompts you to create a shortcut on the desktop. You can launch the program by dragging a csv file and dropping it on the shortcut icon. 

### Command line usage

Alternatively, you can

- launch the program on the command line passing the yWriter project file as an argument, or
- launch the program via a batch file.

usage: `aeon3yw.pyw [--silent] Sourcefile`

#### positional arguments:

`Sourcefile` 

The path of the Aeon Timeline 3 csv export file.

#### optional arguments:

`--silent`  suppress error messages and the request to confirm overwriting

## Prepare your timeline for export

The included installation script installs a "yWriter" template in the Aeon 2 configuration folder. 
The easiest way is to create new timelines based on this template. It provides the entities and event properties that are converted to yWriter by default.

For existing timelines you have two choices:

1. Add or rename the required entities and event properties in the Timeline settings.
2. Customize the *aeon3yw* configuration to fit your timeline.


## csv export from Aeon Timeline 3

- The csv file exported by Aeon Timeline 3 must be **comma**-separated.
- Date format is like **1940-11-27**.
- Time format is like **17:43**.


![Aeon 2 csv export settings](Screenshots/Aeon2_export_settings.png)


## Custom configuration

You can override the default settings by providing a configuration file. Be always aware that faulty entries may cause program errors. 

An optional project configuration file named `aeon3yw.ini` can be placed in your project directory, i.e. the folder containing your yWriter and Timeline project files. It is only applied to this project. Its entries override aeon3yw's built-in constants.

### How to provide/modify a configuration file

The aeon3yw distribution comes with a sample configuration file located in the `sample` subfolder. It contains aeon3yw's default settings and options. You best make a copy and edit it.

- The SETTINGS section mainly refers to "labels", i.e. The csv field contents of the first row, which denote the columns. They might have to be adapted to your specific Aeon project and export settings. If you change them, the program might behave differently than described in the description of the conversion rules below. Make sure the indicated csv fields contain data that can be processed by yWriter.
- The OPTIONS section comprises options for regular program execution. 
- Comment lines begin with a `#` number sign. In the example, they refer to the code line immediately above.

This is the configuration explained: 

```
[SETTINGS]

scene_marker = Yes

# String that indicates an event to be exported as normal
# scene, if "export_all_events" is "No"
# If the scene marker is left blank, all events will be
# imported as normal scenes.
# In this case, the entry looks like "scene_marker ="

scene_label = Scene

# Label of the csv field that contains the "scene_marker"
# indicator.

title_label = Title

# Label of the csv field whose contents are exported
# as the scene's title to yWriter.

start_date_time_label = Start Date

# Label of the csv field whose contents are exported
# as the scene's date/time to yWriter.

end_date_time_label = End Date

# Label of the csv field whose contents are used to
# calculate the scene's duration.

description_label = Description

# Label of the csv field whose contents are exported
# as the scene's description to yWriter.

notes_label = Notes

# Label of the csv field whose contents are exported
# as the scene's notes to yWriter.

tag_label = Tags

# Label of the csv field whose contents are exported
# as the scene's tags to yWriter.

location_label = Location

# Label of the csv field whose contents are exported
# as the scene's locations to yWriter.

item_label = Item

# Label of the csv field whose contents are exported
# as the scene's items to yWriter.

character_label = Participant

# Label of the csv field whose contents are exported
# as the scene's characters to yWriter.

viewpoint_label = Viewpoint

# Label of the csv field whose contents are exported
# as the scene's viewpoint to yWriter.

[OPTIONS]

export_all_events = Yes

# Yes: Export non-scene events as "Notes" type scenes
#      to yWriter.
# No:  Do not export non-scene events to yWriter.
# This option exists only if the scene marker is not
# left blank.

```

Note: Your custom configuration file does not have to contain all the entries listed above. 
The changed entries are sufficient. 

## Conversion rules

The column labels refer to timelines based on the "yWriter" template. 

-   All events with the "Scene" property ticked are converted to regular scenes (*).
-   All events with the "Scene" property not ticked are converted to "Notes" scenes (*).
-   All scenes are placed in a single chapter.
-   All scenes are sorted chronologically (Note: "BC" is not evaluated). 
-   The scene status is "Outline". 
-	The event title is used as scene title (*).
- 	The start date is used as scene date/time, if the start year is 100 or above.
-	The scene duration is calculated by the end date, if the start year is 100 or above.
-	Event tags are converted to scene tags, if any (*).
-   "Descriptions" are imported as scene descriptions, if any (*).
-   "Notes" are used as scene notes, if any (*).
-	"Participants" are imported as characters, if any (*).
-	"Viewpoints" are imported as viewpoint characters, if any (*).
-	"Locations" are imported, if any (*).
-	"Items" are imported, if any (*).

(*) Applies to the default configuration, but can be customized. 


## Installation path

The **install.bat** installation script installs *aeon3yw.pyw* in the user profile. This is the installation path: 

`c:\Users\<user name>\AppData\Roaming\PyWriter\aeon3yw`
    