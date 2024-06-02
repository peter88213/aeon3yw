# aeon3yw
Generate a yWriter project from an Aeon Timeline 3 project file.

For more information, see the [project homepage](https://peter88213.github.io/aeon3yw) with description and download instructions.

## Development

*aeon3yw* is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

## Important

Please note that the program has not yet been extensively tested. To me, it's actually just a proof of concept. I probably won't develop the program further. Feel free to copy the project and modify it to your own liking.

**According to recent user feedback, the Aeon Timeline 3 file format has been changed, so this script might not work for you.**

### Conventions

See https://github.com/peter88213/PyWriter/blob/main/docs/conventions.md

Exceptions:
- No localization is required.
- The directory structure is modified to minimize dependencies.

### Development tools

- [Python](https://python.org) version 3.10
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and [EGit](https://www.eclipse.org/egit/)
- Apache Ant for building the application script

## Credits

- Frederik Lundh published the [xml pretty print algorithm](http://effbot.org/zone/element-lib.htm#prettyprint).

## License

aeon3yw is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
