# PDF-Search-Contents
Python script for indexing PDF contents and search

This is mainly intended for Windows users who need to search PDF contents* on shared drives since the Windows Indexing Service has been proven unreliable.  This can also be useful for those accessing Linux Samba shares.

The create_index script places an index.json file in each of the directories under the defined base_folder.  The create_index script will need write access to each of those folders in order to save the index.

The find_files script allows you to select which directory you want to search in as well as the search string, then click in the results to open the desired file(s).

The commands in make_executable can be ran manually in the terminal to create stand-alone .exe files if desired.

*Scanned PDF's must have had Optical Charactor Recognition(OCR) ran on them in order to be searchable.

