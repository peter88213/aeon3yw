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

The included installation script installs a "yWriter" template in the Aeon 3 configuration folder. 
The easiest way is to create new timelines based on this template. It provides the entities and event properties that are converted to yWriter by default.

For existing timelines you have two choices:

1. Add or rename the required entities and event properties in the Timeline settings.
2. Customize the *aeon3yw* configuration to fit your timeline.


## csv export from Aeon Timeline 3

- The csv file exported by Aeon Timeline 3 must be **comma**-separated.


## Custom configuration

You can override the default settings by providing a configuration file. Be always aware that faulty entries may cause program errors. 

### Global configuration

An optional global configuration file can be placed in the configuration directory in your user profile. It is applied to any project. Its entries override aeon3yw's built-in constants. This is the path:
`c:\Users\<user name>\AppData\Roaming\PyWriter\aeon3yw\config\aeon3yw.ini`
  
The **install.bat** installation script installs a sample configuration file containing aeon3yw's default values. You can modify or delete it. 

### Local project configuration

An optional project configuration file named `aeon3yw.ini` can be placed in your project directory, i.e. the folder containing your yWriter and Timeline project files. It is only applied to this project. Its entries override aeon3yw's built-in constants as well as the global configuration, if any.

### How to provide/modify a configuration file

The aeon3yw distribution comes with a sample configuration file located in the `sample` subfolder. It contains aeon3yw's default settings and options. This file is also automatically copied to the global configuration folder during installation. You best make a copy and edit it.

- The SETTINGS section mainly refers to "labels", i.e. The csv field contents of the first row, which denote the columns. They might have to be adapted to your specific Aeon Timeline setup. If you change them, the program might behave differently than described in the description of the conversion rules below. Make sure the indicated csv fields contain data that can be processed by yWriter.
- Comment lines begin with a `#` number sign. In the example, they refer to the code line immediately above.

This is the configuration explained: 

```
[SETTINGS]

part_number_prefix = Part

# Prefix to the part number in the part's heading.

chapter_number_prefix = Chapter

# Prefix to the chapter number in the chapter's heading.

part_desc_label = Label

# Label of the csv field whose contents are exported
# as the part's description to yWriter.

chapter_desc_label = Label

# Label of the csv field whose contents are exported
# as the chapter's description to yWriter.

scene_desc_label = Summary

# Label of the csv field whose contents are exported
# as the scene's description to yWriter.

scene_title_label = Label

# Label of the csv field whose contents are exported
# as the scene's title to yWriter.

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


```

Note: Your custom configuration file does not have to contain all the entries listed above. 
The changed entries are sufficient. 

## Conversion rules

The column labels refer to timelines based on the "yWriter" template. 

-   All narrative scenes are converted to regular scenes placed in the right chapters.
-   All non-narrative events are converted to "Notes" scenes placed in the "Trash" chapter.
-   Part and chapter headings are generated by adding a number to a customizable prefix.
-   Part and chapter labels are exported as part and chapter descriptions (*).
-   The scene status is "Outline". 
-	The event label is used as scene title (*).
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
    