# aeon3yw
Generate a yWriter project from an Aeon Timeline 3 csv export.

For more information, see the [project homepage](https://peter88213.github.io/aeon3yw) with description and download instructions.

## Development

*aeon3yw* depends on the [pywriter](https://github.com/peter88213/PyWriter) library which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application script

```
.
├── PyWriter/
│   └── src/
│       └── pywriter/
└── aeon3yw/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Conventions

- Minimum Python version is 3.6. 
- The Python **source code formatting** follows widely the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, except the maximum line length, which is 120 characters here.

### Development tools

- [Python](https://python.org) version 3.9
- [Eclipse IDE](https://eclipse.org)
- [PyDev](https://pydev.org) Python development plugin for the Eclipse IDE
- [EGit](https://www.eclipse.org/egit/) Eclipse Team provider for the Git version control system
- [Apache Ant](https://ant.apache.org/) for building the application script

## Credits

- Frederik Lundh published the [xml pretty print algorithm](http://effbot.org/zone/element-lib.htm#prettyprint).

## License

aeon3yw is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
