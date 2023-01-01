[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "features" project](https://github.com/peter88213/aeon3yw/projects/1).

### v1.0.4

- Make it run on old Windows versions: Restore the original pywriter_globals module from PyWriter v5.18.0 to get rid of internationalization code.

Based on PyWriter v5.18.0

### v1.0.3 Prepare for Python 3.11

- Remove "shebang" to make the program run with Python 3.11. 
- Replace deprecated locale.getdefaultlocale() by locale.getlocale()

Based on PyWriter v5.18.0

### v1.0.2 Update setup script

- Change the working dir to the script dir on startup in order to avoid "file not found" error.
- Catch exceptions in the setup script.

Based on PyWriter v5.18.0

### v1.0.1

- Fix a bug in the setup script where the INI file is not installed.
- Improve the code quality.
- Improve the documentation.

Based on PyWriter v5.0.2

### v1.0.0

- Rework the error messaging system.
- Refactor the code.

Based on PyWriter v5.0.0

### v0.6.2  Beta release: Support non-Windows OS

- Move installation and configuration to another location (see instructions for use).

Based on PyWriter v3.28.1

### v0.6.1 Beta release: Enable non-Windows operation 

- Catch an exception that is thrown when evaluating a Windows environment variable under a non-Windows OS.

Based on PyWriter v3.28.1

### v0.6.0 Beta release: Read the .aeon file format 

- Read the native .aeon file format. CSV is optional.

Based on PyWriter v3.28.1

### v0.4.2 Optional update

Apply paeon update to minimize the amount of unused code.

Based on paeon v0.10.1 and PyWriter v3.26.1

### v0.4.1 Alpha release 

- Update libraries and help text.

Based on paeon v0.6.2 and PyWriter v3.26.1

### v0.4.0 Alpha release

- Import character and location properties.

Based on PyWriter v3.24.3 and paeon v0.6.0

### v0.2.4 Alpha release

Process incomplete date/time stamps as possible with Aeon Timeline 3.
Missing months or days are substituted by '01'.

Based on PyWriter v3.24.3 and paeon v0.4.1

### v0.2.3 Alpha release

- Restructure the project to keep reusable code in the external *paeon* library.

Based on PyWriter v3.24.3 and paeon v0.2.0

### v0.2.2 Alpha release 

- Change the default value for invalid date from "-0001-01-01" to "0001-01-01" in order to avoid isoformat errors.

Based on PyWriter v3.24.3

### v0.2.1 Alpha release 

- Update documentation: Use the "import" from yWriter's point of view.

Based on PyWriter v3.24.3

### v0.2.0 Alpha test release

The *yWriter.aeonTpl* template doesn't provide items yet.

Based on PyWriter v3.24.3

