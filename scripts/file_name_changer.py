import os
from os.path import join
import globals
import re

def change_file_names(input_directory : str ):

    for file in os.listdir(input_directory):
        
        if os.path.isdir(os.path.abspath(input_directory) + "/" + file):
            change_file_names(os.path.abspath(input_directory) + "/" + file)
        
        else:

            new_file_name = replace_all_region_data(file)

            if ".cue" in file:

                change_data_in_cue(file, input_directory)
            
            if (check_filename_validity(new_file_name)):
                
                new_file_name = set_file_name_manually(new_file_name)
                change_file_names_manually(input_directory, new_file_name)
                return


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

def change_data_in_cue(file : str, input_directory: str, new_name : str = ""):
    
    default_file = open(os.path.abspath(input_directory) + "/" + file, "r")
    edited_file = open(os.path.abspath(input_directory) + "/" + "temp", "w")

    for line in default_file:

        if file.split(".")[0] in line:
            temp_binary_name = line.replace("FILE \"", "").replace("\" BINARY\n", "")
            if (new_name == ""):
                temp_binary_name = replace_all_region_data(temp_binary_name)
            else:
                temp_binary_name = new_name + ".bin"
            edited_file.write("FILE \"" + temp_binary_name + "\" BINARY\n")

        else:
            edited_file.write(line)


    edited_file.close()
    default_file.close()


    os.rename(os.path.abspath(input_directory) + "/" + "temp",
              os.path.abspath(input_directory) + "/" + file)


def check_filename_validity(name : str) -> bool:
    return (len(name) + 4 > 60)

def set_file_name_manually(file_name : str) -> str:

    name_is_valid : bool = False

    while (not name_is_valid):
        globals.show_message(f'''Current name of files is not compatible with PSIO.
                             Please enter new name of files for game:
                             {file_name}
                             Remark: do not forget about 4 additional symbols for file extension''')

        manual_name = str(input())

        if (len(manual_name) + 4 > 60):
            globals.show_message(f'''Entered file name {manual_name} has more than 60 
                                 symbols with file extension.
                                Try enter new name.''')
        else:
            return manual_name

def change_file_names_manually(input_directory : str, new_file_name : str):

    for file in os.listdir(os.path.abspath(input_directory)):
        file_extension : str = file.split(".")[-1]
        if file_extension == "cue":

            change_data_in_cue(file, input_directory, new_file_name)

        os.rename(os.path.abspath(input_directory) + "/" + file, 
                  os.path.abspath(input_directory) + "/" + new_file_name + "." + file_extension)
    os.rename(os.path.abspath(input_directory), 
              "/".join(os.path.abspath(input_directory).split("/")[:-1]) + "/" + new_file_name)

