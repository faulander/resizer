# ResiZer

ResiZer is a script, which recursively traverses directories and resizes images and deletes unwanted files.

## Description

Given an inputpath, ResiZer will recursively find all imagefiles and resize them.
It will also delete unwanted files.
Please refer to the resizer.ini file, there is an extensive documentation available.

## Getting Started

### Dependencies

* Developed with Python 3.6, should work on every Python 3.x version
* Developed on Linux, it should work on windows aswell

### Installing

* Download or clone the repository
* pip install -r requirements.txt

If you want to run the script inside a docker environment, i have added a working Dockerfile.

### Executing program

* python resizer.py


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Modules used

* Pillow
* Schedule
* Peewee