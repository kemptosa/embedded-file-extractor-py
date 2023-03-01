# embedded file extractor py
 Extracts files embedded within binaries (e.g. .pngs out of .dlls)

# Usage
 Usage is simple: drag a binary file onto the python script. (assuming you have python installed and set as the file handler for .py files)  
 Alternatively, run the python script and enter the file location manually.

 After the file is loaded, the script will automatically search the binary for embedded files and print their locations and sizes to the terminal. The files will also be extracted into the directory containing the python script.

 The script will *not* find files which have been compressed, encoded, encrypted, or otherwise obscured.

# Supported file types
 - [x] png  
 - [x] jpeg/jfif
 - [x] bmp
 - [ ] dds
 - [ ] ...

# Planned Features
 - [ ] Replace images in binary
 - [ ] Better interface
