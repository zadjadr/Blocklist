![Autoupdating blocklist.txt](https://github.com/Xcalizorz/Blocklist/workflows/Autoupdating%20blocklist.txt/badge.svg)

# Blocklist updater

Used with Pihole.

Python `>= 3.6` required (or remove the `f-strings`).

## Usage

1. Append or change the list of urls in `blocklist.txt`
2. `python update.py`


Unreachable `urls` within `blocklist.txt` will be removed from it.

A simple `adlists.list` will be created, aggregating all hosts found.

Now, you can refer to your own github-links in `pihole-admin`.
