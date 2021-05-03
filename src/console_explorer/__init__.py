"""
A Python lib that enables you to load a command-line file explorer for your users !
"""
import shutil
import os
import platform
from copy import deepcopy

def _log(*args, **kwargs):
    print("-"*10, *args, "-"*10, **kwargs)

def _browse(return_type:str="folder", path:str=None, existence_required:bool=False, enable_commands:bool=True,
            handle_same_file:bool=True, cancel_enabled:bool=True, extensions_list:tuple=None):
    """
    :param return_type: folder, filename
    """
    _path = os.getcwd() if path is None else path

    if platform.platform().startswith("Windows"):
        _path = _path.split("\\")
    else:
        _path = _path.split("/")

    user_input = None
    while user_input != "":
        # Prints the path
        print("/".join(_path))

        # Prints all the directories in the folder
        files_list = []
        for element in os.listdir("/".join(_path)):
            if element.startswith("__"): continue
            if os.path.isdir("/".join(_path) + "/" + element):
                print("📁", element)
            else:
                if extensions_list is None or (element.split(".")[-1] in extensions_list):
                    files_list.append("📄 " + element)

        for file in files_list:
            print(file)
        del files_list

        # Ask to which directory go
        user_input = input(">>> ")
        # Output type
        if return_type == "filename":
            if "." in user_input and len(user_input) >= 3 and not "/" in user_input:
                file_path = "/".join(_path) + "/" + user_input
                if (existence_required is True and os.path.exists(file_path))\
                        or existence_required is False:
                    if existence_required is False and handle_same_file is True and os.path.exists(file_path):
                        confirm = "a"
                        while confirm[0].lower() not in ("y", "n"):
                            confirm = input("This file already exists. Are you sure you want to replace it ? (y/n) ")

                        if confirm[0].lower() == "n": continue

                    if extensions_list is None or (file_path.split(".")[-1] in extensions_list):
                        return file_path
                    else:
                        _log("This extension is not valid. The extension should be part of (" + ",".join(extensions_list) + ").")
                        continue
        elif return_type == "folder":
            if user_input == "":
                confirm = "a"
                while confirm[0].lower() not in ("y", "n"):
                    confirm = input("Are you sure you want to select this folder ? (y/n) ")

                if confirm[0].lower() == "n":
                    user_input = " "
                    continue

                return "/".join(_path)

        if user_input == "CANCEL" and cancel_enabled is True: return None

        user_input = user_input.split("/")
        if user_input[-1] == "": user_input.pop()

        # Command handling
        if enable_commands is True:
            matched_command = False
            if user_input[0].split(" ")[0] == "MKDIR":
                user_input[0] = user_input[0].replace("MKDIR ", "", 1)
                try:
                    os.mkdir("/".join(_path) + "/" + "/".join(user_input))
                except Exception:
                    _log("An error occurred.")
                matched_command = True
            elif user_input[0].split(" ")[0] == "RMDIR":
                user_input[0] = user_input[0].replace("RMDIR ", "", 1)
                try:
                    os.rmdir("/".join(_path) + "/" + "/".join(user_input))
                except PermissionError:
                    _log("Permission error, cannot delete folder.")
                except OSError:
                    confirm = "a"
                    while confirm[0].lower() not in ("y", "n"):
                        confirm = input("This directory is not empty. Are you sure you want to delete it ? (y/n) ")

                    if confirm[0].lower() == "n":
                        continue

                    shutil.rmtree("/".join(_path) + "/" + "/".join(user_input))
                except Exception:
                    _log("An error occured.")
                matched_command = True

            if matched_command is True:
                continue
        else:
            if user_input[0].split(" ")[0] in ("MKDIR", "RMDIR"):
                _log("Commands are disabled.")
                continue

        # Modifies the path
        temp_path = deepcopy(_path)  # Saving the old path in case of error
        # Fetches all the folders in the input
        for folder in user_input:
            if folder == "..":  # Goes to parent folder
                _path.pop()
            elif folder in (".", ""):  # Does nothing
                pass
            else:  # Adds a new folder to the path
                _path.append(folder)

        # Checks if exists
        if not os.path.exists("/".join(_path)):
            _log("Unexisting path.")
            _path = deepcopy(temp_path)

def browse_for_file(path=None, existence_required:bool=False, handle_same_file:bool=True, enable_commands:bool=True, cancel_enabled:bool=True, extensions_list:tuple=None):
    """
    Browses for a file and returns its path.
    :param path: Indicates a default path.
    :param existence_required: Boolean indicating whether or not the file should already exist.
    :param handle_same_file: Boolean indicating whether or not to warn the user if the file he selected already exists. Automatically False if existence_required is True.
    :param enable_commands: Boolean indicating whether or not commands (MKDIR/RMDIR) are enabled.
    :param extensions_list: A tuple of extensions the user can open. By default, any.
    :param cancel_enabled: Boolean indicating if the CANCEL command should be enabled or not.
    """
    return _browse("filename", path, existence_required=existence_required, handle_same_file=handle_same_file, enable_commands=enable_commands, cancel_enabled=cancel_enabled, extensions_list=extensions_list)

def browse_for_folder(path=None, enable_commands:bool=True, cancel_enabled:bool=True):
    """
    Browses for a folder and returns its path.
    :param path: Indicates a default path.
    :param enable_commands: Boolean indicating whether or not commands (MKDIR/RMDIR) are enabled.
    :param cancel_enabled: Boolean indicating if the CANCEL command should be enabled or not.
    """
    return _browse("folder", path, enable_commands=enable_commands, cancel_enabled=cancel_enabled)

