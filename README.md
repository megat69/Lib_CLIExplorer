# CLI_Explorer
A Python lib that enables you to load a command-line file explorer for your users !

This lib allows you to ask the user to look for a specific file, folder, or a location in which to save a file !<br/>
The lib also comes with a built-in duplicate system, which lets you or the user choose what to do if a file with the same filename already exists, and much more features !

## Install
### Install from PyPI
To install the library, just type `pip install python-console-explorer` and this should be ok.

Visit [PyPI](https://pypi.org/project/python-console-explorer/) for more info.

### Install from source
Just download the file at [this link](https://github.com/megat69/Lib_CLIExplorer/blob/main/src/console_explorer/__init__.py), and import it in your project.

## Usage
*See [examples](https://github.com/megat69/Lib_CLIExplorer/tree/main/examples) if wanted.*

The library gives access to two functions. The first allows to browse for a file, the second for a folder.

### The `browse_for_file` function
This function will return the path to a file. This file might be non-existent, if the parameter `existence_required` is set to False (default).

Parameters :
- `path` : The default path in which the explorer will be opened.
- `existence_required` : Boolean indicating whether or not the file should already exist.
- `handle_same_file` : Boolean indicating whether or not to warn the user if the file he selected already exists.
  - Automatically `False` if existence_required is True.
- `enable_commands` : Boolean indicating whether or not commands (`MKDIR`/`RMDIR`) are enabled.
- `extensions_list` : A tuple of extensions the user can open. By default, any.
- `cancel_enabled` : Boolean indicating if the CANCEL command should be enabled or not.

### The `browse_for_folder` function
This function will return the path to a folder.

Parameters :
- `path` : The default path in which the explorer will be opened.
- `enable_commands` : Boolean indicating whether or not commands (`MKDIR`/`RMDIR`) are enabled.
- `cancel_enabled` : Boolean indicating if the CANCEL command should be enabled or not.

## Example
**Creating a basic text editor.**

This program is a text editor, the user will input each line, one by one, then type `EXIT` when he's finished.

Afterwards, he will look for a place to save the file.

*[File available on GitHub](https://github.com/megat69/Lib_CLIExplorer/blob/main/examples/saver.py)*

```python
from console_explorer import *

# Creating the two required variables
text = ""  # The file's text
user_input = ""  # The user input (just initialized, here)

# Looping until the user types 'EXIT'
while user_input != "EXIT":
    # Asking him a line
    user_input = input("")
    # If the line is not 'EXIT' (which would mean we are done writing the text), we add the
    # inputted line to the text
    if not user_input == "EXIT": text += user_input + "\n"

# We ask the user to choose the file destination.
# Also, we only want it to be a plain text (.txt) file or Markdown file (.md)
file_to_save_in = browse_for_file(extensions_list=("txt", "md"))

# If the user cancelled the save, we simply pass
if file_to_save_in is None:
    pass
# Otherwise, we open the file he selected, and we put the text inside.
else:
    with open(file_to_save_in, "w") as file:
        file.write(text[:-1])
```
