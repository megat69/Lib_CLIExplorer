import os
import platform
from copy import deepcopy

path = os.getcwd()

if platform.platform().startswith("Windows"):
    path = path.split("\\")
else:
    path = path.split("/")

user_input = None
while user_input != "":
    # Prints the path
    print("/".join(path))

    # Prints all the directories in the folder
    files_list = []
    for element in os.listdir("/".join(path)):
        if element.startswith("__"): continue
        if os.path.isdir("/".join(path) + "/" + element):
            print("📁", element)
        else:
            files_list.append("📄 " + element)

    for file in files_list:
        print(file)
    del files_list

    # Ask to which directory go
    user_input = input(">>> ")
    if user_input == "": break
    user_input = user_input.split("/")

    # Modifies the path
    temp_path = deepcopy(path)  # Saving the old path in case of error
    # Fetches all the folders in the input
    for folder in user_input:
        if folder == "..":  # Goes to parent folder
            path.pop()
        elif folder in (".", ""):  # Does nothing
            pass
        else:  # Adds a new folder to the path
            path.append(folder)

    # Checks if exists
    if not os.path.exists("/".join(path)):
        print("Unexisting path.")
        path = deepcopy(temp_path)
