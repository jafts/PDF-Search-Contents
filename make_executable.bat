# Use pyinstaller to create a stand-alone executable and assign it an icon.
# More about pyinstaller at https://pyinstaller.org/ and https://github.com/pyinstaller

pyinstaller --onefile --windowed --icon=c:\my_icon_directory\my_icon.ico c:\script_directory\find_files.py

pyinstaller --onefile --windowed c:\script_directory\create_index.py
