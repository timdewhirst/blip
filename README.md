# blip

A backup utility for blipfoto.com

Sometimes, just sometimes, you might want to backup your blips: this does a very basic job. It will:
* create a new directory with your username
* starting from the most recent entry, work backwards until no previous entry is found
* for each entry save:
** content.json (the page content including comments, ratings and metadata)
** image.jpg (the standard resolution image)

There are some limitations:
* I didn't figure out how to get the high-res image
* it will sleep for 2s between fetching each entry to avoid spamming blipfoto's servers

To run you'll need python3 (2 should probably work too) and it should be run as:

* python3 previewer.py <username> (for me: tpd)

I've only tested this on Linux; if anyone would like to test and fix on OS X or windows please do.
