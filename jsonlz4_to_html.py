#!/usr/bin/env python3
"""

Converts Mozilla Firefox archived bookmarks .JSONLZ4 to .HTML

Bookmarks, implicitly archived in Mozilla Firefox files .JSONLZ4,
can be converted to .HTML format quite similar to the format
Firefox uses itself for Import/Export bookmarks.
So you can add them to a new branch without nesessity of replacing
all of your old bookmarks.

Usage in Windows:
1. Edit drop_onto_me.bat as you like
2. Drag_n_Drop source file onto drop_onto_me.bat
3. Resulting file(s) will be situated at the same place as input file.

"""
import sys
import os.path
import json
import argparse
try:
    import lz4.block as lz4
except ImportError:
    print("Please install 'lz4' packet via entering 'pip install lz4' in Windows PowerShell "
          "or command line.")
    sys.exit(2)

SEVICE_GUIDS = ('mobile______', 'unfiled_____', 'toolbar_____', 'menu________', 'root________')
HEADING = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Root</H1>\n\n'''
BRANCH = '{indent}<DT><H3 ADD_DATE="{added}" LAST_MODIFIED="{modif}" {specials_string}>{title}</H3>\n' \
         '{indent}<DL><p>\n'
BOOKMARK = '{indent}<DT><A HREF="{href}" ADD_DATE="{added}" LAST_MODIFIED="{modif}" ICON_URI="{icon_uri}">{title}</A>\n'
BRANCH_TAIL = '{indent}</DL><p>\n'


def bmks_from_collection_to_list(source_dict: dict, list_dst: list):
    def recursive_parse(children_list, dst, father_guid, father_level):
        # dive into 'children' list
        for nth in children_list:
            nth.update({'level': int(father_level)+1,
                        'father_guid': father_guid,
                        'has_children': bool(nth.get('children', False))})
            dst.append(clear_data(nth))                                           # add each
            if nth['typeCode'] == 2 and nth.get('children'):
                # TODO keep bookmarks order by sorting nth['children'] by "index" field
                recursive_parse(nth['children'], dst, nth['guid'], nth['level'])  # recurse branch

    def clear_data(input_entry: dict):
        # Returns all fields except 'children' one
        return {x: input_entry[x] for x in input_entry if x != 'children'}

    # -----------------------------------------------------
    src = source_dict.copy()
    assert isinstance(src, dict)
    assert isinstance(list_dst, list)
    assert src.get('guid') in SEVICE_GUIDS
    assert src.get('children')
    # TODO convert non-bookmarks(session or any structure) Mozilla archives to usable bookmark list

    # Initial configuration of root
    # root has level = 0
    src.update({'level': 0, 'father_guid': '0', 'has_children': True})          # add root
    list_dst.append(clear_data(src))

    # Recursive fn
    recursive_parse(src['children'], list_dst, src['guid'], src['level'])


def bmk_to_html_strings(source_dict: dict, list_dst: list):
    def indentation(src: dict):
        # 1 level => 4 spaces
        # Root has level 0
        return '    ' * src['level'] if src.get('level') else ''

    def lastlevel_byindent(l_in):
        # Get last level counting leading spaces in last string in list
        if not l_in or not isinstance(l_in, list):
            return 0
        return (len(l_in[-1]) - len(l_in[-1].lstrip(" "))) // 4

    # ----------------------------------------------
    assert isinstance(source_dict, dict)
    assert source_dict.get('typeCode') in (1, 2)
    assert source_dict.get('level')
    bmk = source_dict.copy()

    if bmk['level'] < lastlevel_byindent(list_dst):  # indentation lower - branch tail string added
        list_dst.append(BRANCH_TAIL.format(indent=indentation(bmk)))

    if bmk.get('typeCode') == 2:
        if bmk.get('has_children'):
            # '{indent}<DT><H3 ADD_DATE="{add}" LAST_MODIFIED="{modif}" {specials_string}>{title}</H3>\n' \
            # '{indent}<DL><p>
            # TODO special folder names recognition          # '''PERSONAL_TOOLBAR_FOLDER="true"''
            list_dst.append(BRANCH.format(indent=indentation(bmk),
                                          added=str(bmk.get('dateAdded'))[:10],
                                          modif=str(bmk.get('lastModified'))[:10],
                                          specials_string='',
                                          title=bmk.get('title')))
        else:
            pass  # <-- empty branches not included
    elif bmk.get('typeCode') == 1:
        # '{indent}<DT><A HREF="{href}" ADD_DATE="{added}" LAST_MODIFIED="{modif}" ICON_URI="{icon_uri}">{title}</A>\n'
        list_dst.append(BOOKMARK.format(indent=indentation(bmk),
                                        href=bmk.get('uri', ''),
                                        added=str(bmk.get('dateAdded'))[:10],
                                        modif=str(bmk.get('lastModified'))[:10],
                                        icon_uri=bmk.get('iconuri', ''),
                                        title=bmk.get('title')))
    else:
        return


def bat_workaround_plus(in_str):
    allowed_exts = {".jsonlz4", ".baklz4"}
    print (in_str)

    dirname = os.path.dirname(in_str)
    basename = os.path.basename(in_str)
    root, ext = os.path.splitext(basename)

    if ext:
        if ext.lower() not in allowed_exts:
            raise ValueError(f"Unsupported extention: {ext} (.jsonlz4 or .baklz4 expected)")
        else:
            if os.path.exists(in_str):
                return in_str
            else:
                raise FileNotFoundError(f"File not found: {in_str}")
    else:
        for omitted_tail in ("=", "=="):
            for e in allowed_exts:
                if os.path.exists(expected_path := os.path.join(dirname, root + omitted_tail + e)):
                    print(f"Workaround applied: restored '{omitted_tail + e}' → {expected_path}")
                    return expected_path
        raise FileNotFoundError(f"No bookmarks file with = or == guessed.")


# ================================================================
def main():
    arg_parse = argparse.ArgumentParser(description="JSONLZ4 bookmarks to HTML converter",
                                        epilog="Bookmarks, implicitly archived in Mozilla Firefox files .JSONLZ4,\n"
                                               "can be converted to .HTML format quite similar to the format\n"
                                               "Firefox uses itself for Import/Export bookmarks\n"
                                               "\n"
                                               "Resulting file will be situated at the same place as input file.",
                                        formatter_class=argparse.RawTextHelpFormatter)
    arg_parse.add_argument("input_filename",
                           metavar='''"input_filename"''',
                           help="source filename with path or not\n"
                                '''Make shure that it's enclosed in double quotation marks ""\n'''
                                "on Windows systems, where file path can contain spaces")
    arg_parse.add_argument("-t", action="store_true", default=False,
                           help="save decoded html if bookmarks found")
    arg_parse.add_argument("-j", action="store_true", default=False,
                           help="save decoded json")
    arg_parse.add_argument("-o", action="store_true", default=False,
                           help="overwrite output file(s) if exists")
    arg_parse.add_argument("-s", action="store_true", default=False,
                           help="silent mode for use in scripts")
    args = arg_parse.parse_args()
    i_fpname = os.path.abspath(args.input_filename)

    # one of the strange issues of Windows is in incapability to hand filename with "=" (and some
    # other chars) thru batch file arguments to script's arguments, IF full name not contains
    # at least one space symbol. It is due to twisted handling double quotation marks "" around
    # dragged_and_dropped paths in Windows.
    # The workaround of issue with omitted '==' symbols in filename dropped to .bat below
    i_fpname = bat_workaround_plus(i_fpname)

    o_h_fpname = "".join(i_fpname.split(".")[:-1]) + ".html"
    o_j_fpname = "".join(o_h_fpname.split(".")[:-1]) + ".json"

    if not os.path.exists(i_fpname):
        sys.exit(3)
    if not args.o and os.path.exists(o_h_fpname):
        sys.exit(4)

    # Open JSONLZ4-like file
    # decode to utf-8
    with open(i_fpname, 'rb') as fin:
        if not fin.read(8) == b'mozLz40\0':
            raise ValueError("Not a valid Mozilla .jsonlz4 file")
        header_plus = fin.read(100)
        if b"version" in header_plus or b"guid" not in header_plus:
            raise ValueError("Given .jsonlz4 is not a bookmarks archive file.")
        fin.seek(8)  # rewind to after header

        b_data = lz4.decompress(fin.read())
        utf8_str_data = b_data.decode('utf-8')
        if not args.s:
            print("\nInput got from file:")
            print(i_fpname)
            print("\n...and just decoded")

    # Open .json variant for testing purposes
    # with open("bookmarks-2022-03-11.json", 'r', encoding='utf-8') as fin:
    #     c_bookmarks = json.load(fin)
    c_bookmarks = json.loads(utf8_str_data)

    # Save indented .json variant
    if args.j:                                              # in json-mode
        with open(o_j_fpname, 'w', encoding='utf8') as fout:
            fout.write(json.dumps(c_bookmarks, indent=4))
            if not args.s:
                print("\nOutput .json file saved as:")
                print(o_j_fpname)
            if not args.t:                                  # in only-json-mode  exit here
                sys.exit(0)

    # Save .html file variant
    if args.t:
        l_bookmarks = []
        bmks_from_collection_to_list(c_bookmarks, l_bookmarks)  # transrorm to plain list of entries
                                                                # with additional fields
        l_html_strings = []
        for bmk in l_bookmarks[1:]:  # now root is not included
            bmk_to_html_strings(bmk, l_html_strings)            # format each entry data to text
                                                                # and add to list of strings
        with open(o_h_fpname, 'w', encoding='utf-8') as fout:
            fout.write(HEADING)
            fout.write('<DL><p>\n')
            fout.writelines(l_html_strings)
            fout.write('</DL>\n')
            if not args.s:
                print("\nOutput .html file written:")
                print(o_h_fpname)

    sys.exit(0)


# ================================================================
if __name__ == "__main__":
    main()
