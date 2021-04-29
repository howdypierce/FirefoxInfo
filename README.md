# Firefox Info

The problem: When using Firefox on the Mac, it would be convenient to
be able to access certain information about the browser state from
other programs. With Google Chrome and Safari, you can easily get this
information via AppleScript, but Firefox has tied itself in knots and
doesn't have reasonable AppleScript support.

In particular, I have a keyboard shortcut (build using
[Alfred](https://www.alfredapp.com/) which will paste the URL and
title from the active browser, in Markdown format, into the active
window. This is super-convenient when doing research on the Web, and
storing your notes in a notetaking program like (Bear)[https://bear.app/]

The solution is to parse Firefox's session info files. Unfortunately
the format of these files is a bit arcane (and is subject to change
from release to release). Also, the browser only writes the files
every 10 seconds or so, so therefore the information might be slightly
out of date.

The information documented here is current as of April 2021 and
Firefox version 88.

## File format

Firefox records session data in its profile folder, typically located
at `~/Library/Application Support/Firefox/Profiles/<profile
folder>`. Within this directory, the following files are of interest:

* `sessionstore.jsonlz4`: The state of the browser during the last
  shut down. Typically only present when the browser is _not_ running.

* `sessionstore-backups/recovery.jsonlz4`: The current state of the
  browser. Typically only present when the browser _is_ running. This
  is the file we're most interested in.

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
