# Firefox Info

The problem: When using Firefox on the Mac, it would be convenient to
be able to access certain information about the browser state from
other programs. With Google Chrome and Safari, you can easily get this
information via AppleScript, but Firefox has tied itself in knots and
doesn't have reasonable AppleScript support.

My paricular need is that I often use [Bear](https://bear.app) to take
notes from the Web. I wanted to have a hotkey that would insert at the cursor
the current URL and page title, from the frontmost/active Firefox tab, in Markdown format. 

So, in this directory you will find a workflow built using [Alfred](https://www.alfredapp.com/). Currently there are two ways of accessing it:

1. You can type the keyword 'url' into Alfred, at which point you'll get a whole lot of options for copying or inserting the URL in plain format, the URL in Markdown format, or opening the current Firefox page in either Google Chrome or Safari.

2. If you use Bear, while in Bear you can use the hotkey shift-control-M to insert the URL and title, in Markdown format, at the cursor.

Although I have wrapped this up as an Alfred workflow, I tried to write the Python file `FFI.py` in a way that would be useful outside the Alfred context.

## How it works
Because Firefox doesn’t support AppleScript in any reasonable way, FFI.py parses Firefox's session info files. Unfortunately the format of these files is a bit arcane (and is subject to change from release to release). Also, the browser only writes the files every 10 seconds or so, so therefore it is possible for the information might be slightly out of date.

The information documented here is current as of April 2021 and
Firefox version 88.

## File format

Firefox records session data in its profile folder, located
at `~/Library/Application Support/Firefox/Profiles/<profile
folder>`. Within this directory, the following files are of interest:

* `sessionstore.jsonlz4`: The state of the browser during the last
  shut down. Typically only present when the browser is _not_ running.

* `sessionstore-backups/recovery.jsonlz4`: The current state of the
  browser. Typically only present when the browser _is_ running. This
  is the file we're interested in.

* `sessionstore-backups/recovery.baklz4`: The previous version of recovery.jsonlz4

* `sessionstore-backups/previous.jsonlz4`: The state of the browser during the second to last shut down.

* `sessionstore-backups/upgrade.jsonlz4-[timestamp]` - The state of the browser before an upgrade

[source](https://www.foxtonforensics.com/blog/post/analysing-firefox-session-restore-data-mozlz4-jsonlz4)


Unfortunately, these jsonlz4 files are not decryptable by normal Unix
tools.  The file format is as follows:

* The first 8 bytes are the magic number `mozLz40\0`

* Next 4 bytes are the size of the decompressed file, in little Endian
  order.

Fortunately the Python `lz4` package will decompress this file after
you strip off the first 8 bytes.
