import os 
import globals
import re

def change_file_names(input_directory : str):

    for file in os.listdir(input_directory):
        new_file_name = replace_all_region_data(file)

        if ".cue" in file:

            change_data_in_cue(file, input_directory)

        os.replace(os.path.abspath(input_directory) + "/" + file, 
                   os.path.abspath(input_directory) + "/" + new_file_name)


def replace_all_region_data(file_name :str):
    file_name = file_name.replace(" (Europe)", "")
    file_name = file_name.replace(" (USA)", "")
    file_name = file_name.replace(" (Japan)", "")
    file_name = file_name.replace(" (Europe, Australia)", "")

    temp_file_name = re.split(r" \(En.*?\)", file_name)

    if len(temp_file_name) > 1:

        file_name = temp_file_name[0] + temp_file_name[-1]
    
    file_name = file_name.replace(" .", ".")

    return file_name

def change_data_in_cue(file : str, input_directory: str):
    
    default_file = open(os.path.abspath(input_directory) + "/" + file, "r")
    edited_file = open(os.path.abspath(input_directory) + "/" + "temp", "w")

    for line in default_file:

        if file.split(".")[0] in line:
            temp_binary_name = line.replace("FILE \"", "").replace("\" BINARY\n", "")
            temp_binary_name = replace_all_region_data(temp_binary_name)
            edited_file.write("FILE \"" + temp_binary_name + "\" BINARY\n")

        else:
            edited_file.write(line)


    edited_file.close()
    default_file.close()


    os.rename(os.path.abspath(input_directory) + "/" + "temp",
              os.path.abspath(input_directory) + "/" + file)


