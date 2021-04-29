#!/usr/bin/env python3
#
# Get information about the currently-running Firefox instance on the
# Mac, by parsing its session restore files.
#
# This code is current as of Firefox 88 and macOS "Catalina" 10.15.7
# as of April 2021
#
# You will need pip install lz4
#
# Based on / inspired by the following code
#   https://github.com/albertz/foreground_app_info/blob/master/mac/app-scripts/url%20of%20Firefox.py
#   https://unix.stackexchange.com/questions/326897/how-to-decompress-jsonlz4-files-firefox-bookmark-backups-using-the-command-lin

import os
import glob
import lz4.block as lz4
import json
import sys


class FirefoxInfo(object):
    """Class to represent info about the currently running Firefox session.

    Works by parsing Firefox's proprietary session restore files.
    """

    profile_dir="~/Library/Application Support/Firefox/Profiles/*/"
    session_file="sessionstore-backups/recovery.jsonlz4"
    ffox_json_dict={}

    def __init__(self):
        """Initialize a FirefoxInfo instance. State is read at the time of
        instantiation. Then use getter functions to get info about the
        Firefox state.
        """
        # find session file: most recent file that matches the glob
        sess_files = []
        glob_spec = os.path.join(self.profile_dir, self.session_file)
        glob_spec = os.path.expanduser(glob_spec)
        for sf in glob.glob(glob_spec):
            sess_files.append((os.stat(sf).st_mtime, sf))

        sess_file = open(max(sess_files)[1], 'rb')
        assert sess_file.read(8) == b'mozLz40\0'
        self.ffox_json_dict = json.loads(lz4.decompress(sess_file.read()))
        sess_file.close()

    def get_selected_url(self):
        """Return (url, title) for the selected tab of the selected window"""

        selectedWindow = self.ffox_json_dict["selectedWindow"]
        w = self.ffox_json_dict["windows"][selectedWindow - 1]
        selectedTab = w['selected']
        tab = w["tabs"][selectedTab - 1]

        url = tab["entries"][-1]["url"]
        title = tab["entries"][-1]["title"]

        return (url, title)


def add_item(d, title, subtitle, arg, output, iconpath=None):
    "Returns a Python dict meeting Alfred's format"
    item = {"title":title,
            "subtitle":subtitle,
            "arg":arg,
            "variables":{"output_type": output}}
    if iconpath:
        item["icon"] = {"type": "fileicon", "path": iconpath}

    d["items"].append(item)


def main(output_type):
    """Ties into Alfred.

    output_type is one of
       script_filter   -- output the JSON needed to make Alfred list interactive options
       markdown        -- output the Markdown format
       url             -- output just the URL
    """
    ffi = FirefoxInfo()
    (url, title) = ffi.get_selected_url()
    markdown = f"[{title}]({url})"

    if (output_type == "script_filter"):
        d = {"items":[], "rerun": 1}

        add_item(d, "Insert URL", url, url, "insert")
        add_item(d, "Insert URL as Markdown", url, markdown, "insert")
        add_item(d, "Copy URL", url, url, "copy")
        add_item(d, "Copy URL as Markdown", url, markdown, "copy")
        add_item(d, "Open in Google Chrome", url, url, "chrome", "/Applications/Google Chrome.app")
        add_item(d, "Open in Safari", url, url, "safari", "/Applications/Safari.app")

        print(json.dumps(d))

    elif (output_type == "markdown"):
        print(markdown)
        
    elif (output_type == "url"):
        print(url)


if __name__ == u"__main__":
    main(sys.argv[1])

