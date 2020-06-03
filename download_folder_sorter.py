import os
import shutil
from pathlib import Path
import send2trash

# Finds the path to the Downloads folder to get an end result of C:\Users\USERNAME\Downloads
home = str(Path.home())
path = os.path.join(home, 'Downloads')

# A list of all unsorted files within the Downloads folder
file_list = os.listdir(path)

# The dictionary of file extensions in use
file_directory = {}


# Goes through each file in the file list and updates the dictionary of file extensions if any are missing
def update_dictionary():
    for file in file_list:

        # Checks if a file extension folder is present and updates the dictionary
        if '_folder' in file:
            folder_split = file.split('_')
            file_directory.update({folder_split[0]: file})

        # Checks if a file extension is present and moves on or not and updates the dictionary along with creating
        # the necessary folder
        elif '.' in file:
            file_split = file.split('.')
            extension = file_split[len(file_split) - 1]

            if extension not in file_directory:
                file_directory.update({extension: extension + '_folder'})


# Creates file extension folders based on dictionary entries
def create_folders():
    for file in file_directory:
        folder = file_directory.get(file)
        folder_path = os.path.join(path, folder)

        # Creates folders if one does not already exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


# Goes through each unsorted file in the Downloads folder and moves them to designated folder
def move_files():
    for file in file_list:
        if '.' in file:
            file_split = file.split('.')
            extension = file_split[len(file_split) - 1]
            folder = file_directory.get(extension)

            # If there is a duplicate file in folder, the new file overwrites the old and the extra listing
            # is sent to the recycle bin
            if os.path.exists(os.path.join(path, folder, file)):
                shutil.copy(os.path.join(path, file), os.path.join(path, folder))
                send2trash.send2trash(os.path.join(path, file))

            # If the file does not exist in folder, file is moved to destination
            else:
                shutil.move(os.path.join(path, file), os.path.join(path, folder))


update_dictionary()
create_folders()
move_files()
