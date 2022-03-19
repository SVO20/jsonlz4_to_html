# JSONLZ4 to HTML converter
for Mozilla Firefox archived bookmarks.

## Install, Requirements
1. Copy files or clone repo
2. Make shure `Python` installed in your system
3. Install `lz4` lib by:  `pip install lz4`
4. Windows can ask for install additional requiremests for `lz4`. Say yes to Windows.

## Usage in command line

`python jsonlz4_to_html.py [-h] [-t] [-j] [-o] [-s] "input_filename"`

or


`drop_onto_me.bat "input_filename"`


## Usage under Windows GUI
1. **Edit** `drop_onto_me.bat` as you like to prefer action(s)
2. Then **Drag_n_Drop** input .jsonlz4 or .baklz4 onto `drop_onto_me.bat`. Batch accepts only one file at the time.
3. Resulting file(s) will be situated **at the same place as input file**.

## Keys and Parameters
Help:

`python jsonlz4_to_html.py -h`

Help output:
```
jsonlz4_to_html.py -h [-t] [-j] [-o] [-s] "input_filename"

JSONLZ4 bookmarks to HTML converter

positional arguments:
"input_filename"  source filename with path or not
Make shure it's enclosed in double quotation marks " "
on Windows systems, where file path can contain spaces

optional arguments:
-h, --help        show this help message and exit
-t                save decoded html if bookmarks found
-j                save decoded json
-o                overwrite output file(s) if exists
-s                silent mode for use in scripts

Bookmarks, implicitly archived in Mozilla Firefox files .JSONLZ4,
can be converted to .HTML format quite similar to the format
Firefox uses itself for Import/Export bookmarks

Resulting file will be situated at the same place as input file.
```
