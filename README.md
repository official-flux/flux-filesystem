# flux-filesystem
A custom 16 bit file system designed to support my architecture.
- Written in python.
- Simple
- Lightweight

CONS:
- max 64 kilobytes
- each file maximum 4 bytes. (Registry like)

*How it works?*
- each metadata is 256 bytes long.
- 8 byte each file.
-  {
-    4 bytes = name,
-    2 bytes = start_pos,
-    2 bytes = end_pos
-  }
- in each directory or sub directory, there are 32 files/folders.
- $inf file indicate each file/folder type.
- in $inf file there are 32 bytes, each byte represents a file/folder, 0 for file, 1 for folder.
- a folder in this filesystem is a file, it's content is metadata.
- feel free to contribute to this file system, by writing drivers, etc..

