from src.console_explorer import *

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
