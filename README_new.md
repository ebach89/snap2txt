# Snap2Txt

This is modified version of original Snap2Txt (https://github.com/vorniches/snap2txt)

Modifications were done, because another workflow is supposed to be used

## Workflow

Usage of whitelist is supposed from the first glance.
Whitelist is formed like:
```
cmd/Makefile
cmd/some.c
```
Its content can be collected by various bash oneliners, like `git diff --stat` +
`awk` or by means of `find`-tool's specific patterns.

Then the script is run in such way
```
export PYTHONPATH="$PYTHONPATH:/path/to/the/rootdir/of/snap2txt"
python3 snap2txt/snap2txt/__main__.py --wl path/to/.wl
```
