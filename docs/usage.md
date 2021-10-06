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

## Set up your timeline for export

The aeon3yw distribution comes with a "yWriter.aeonTpl" Aeon 3 template in the "sample" folder. You can install it via the *Aeon Timeline Preferences*.

![Custom Templates settings](https://raw.githubusercontent.com/peter88213/aeon3yw/main/docs/Screenshots/import_template.png)

The easiest way is to create new timelines based on this template. It provides the required narrative strucuture and the "Viewpoint" character role.

For existing timelines you have two choices:

### First option: Add or rename the required properties in the Timeline settings.

Open the Timeline Settings. 

In the "Narrative" settings select "Outline Style" as numbering system. Make sure that at least chapters are auto assigned to "folders", and scenes are auto assigned to "other types". 

![Narrative settings](https://raw.githubusercontent.com/peter88213/aeon3yw/main/docs/Screenshots/narrative_settings.png)

In the "Advanced settings" make sure a "Viewpoint" relationship exists for characters that can be assigned to events. The easiest way is to rename an existing relationship, e.g. "Observer". 

![Relationship settings](https://raw.githubusercontent.com/peter88213/aeon3yw/main/docs/Screenshots/advanced_settings.png)


### Second option: Customize the *aeon3yw* configuration to fit your timeline.

See [below](#custom-configuration)


## csv export from Aeon Timeline 3

- The csv file exported by Aeon Timeline 3 must be **comma**-separated.
- At least the "Event" and "Narrative Folder" checkboxes must be ticked.

![Aeon 3 Export settings](https://raw.githubusercontent.com/peter88213/aeon3yw/main/docs/Screenshots/csv_export.png)


## Custom configuration

You can override the default settings by providing a configuration file. Be always aware that faulty entries may cause program errors. 

### Global configuration

An optional global configuration file can be placed in the configuration directory in your user profile. It is applied to any project. Its entries override aeon3yw's built-in constants. This is the path:
`c:\Users\<user name>\AppData\Roaming\PyWriter\aeon3yw\config\aeon3yw.ini`
  
### Local project configuration

An optional project configuration file named `aeon3yw.ini` can be placed in your project directory, i.e. the folder containing your yWriter and Timeline project files. It is only applied to this project. Its entries override aeon3yw's built-in constants as well as the global configuration, if any.

### How to provide/modify a configuration file

The aeon3yw distribution comes with a sample configuration file located in the `sample` subfolder. It contains aeon3yw's default settings and options. You can copy this file to the global configuration folder and edit it.

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

# Label of the csv field whose contents are imported
# as the part's description to yWriter.

chapter_desc_label = Label

# Label of the csv field whose contents are imported
# as the chapter's description to yWriter.

scene_desc_label = Summary

# Label of the csv field whose contents are imported
# as the scene's description to yWriter.

scene_title_label = Label

# Label of the csv field whose contents are imported
# as the scene's title to yWriter.

notes_label = Notes

# Label of the csv field whose contents are imported
# as the scene's notes to yWriter.

tag_label = Tags

# Label of the csv field whose contents are imported
# as the scene's tags to yWriter.

location_label = Location

# Label of the csv field whose contents are imported
# as the scene's locations to yWriter.

item_label = Item

# Label of the csv field whose contents are imported
# as the scene's items to yWriter.

character_label = Participant

# Label of the csv field whose contents are imported
# as the scene's characters to yWriter.

viewpoint_label = Viewpoint

# Label of the csv field whose contents are imported
# as the scene's viewpoint to yWriter.


```

Note: Your custom configuration file does not have to contain all the entries listed above. 
The changed entries are sufficient. 

## Conversion rules

The column labels refer to timelines based on the "yWriter" template. 

-   All narrative scenes are converted to regular scenes placed in the right chapters.
-   All non-narrative events are converted to "Notes" scenes placed in a "Notes" chapter named "Other events".
-   Part and chapter headings are generated by adding a number to a customizable prefix.
-   Part and chapter labels are imported as part and chapter descriptions (*).
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
    