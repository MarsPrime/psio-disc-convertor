import os
import sys
import subprocess
import shutil
import re

import image_creator
import globals
import file_name_changer

import colorama

def main(arguments : list):

    colorama.init()

    if (not check_arguments_validity(arguments)):
        return
    
    input_directory = os.path.abspath(arguments[1])
   

    # set system console version
    format_mode = check_menu_console_version()

   # # set ouput directory
    output_directory = set_output_directory(arguments)

    # delete output directory to prevent errors with overwriting
    shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    # select path of disc images
    input_directory_files: list = os.listdir(input_directory)

    # create dictonary with all .cue files and theirs .bin files quantity
    cue_files = scan_files(sorted(input_directory_files))


    # converting funcrion
    convert_files(cue_files, input_directory, output_directory, format_mode)

    file_name_changer.change_file_names(output_directory)

# check all given arguments
def check_arguments_validity(arguments : list) -> bool: 

    if (not check_input_path(arguments[1])):

        globals.show_message("Invalid argument for input directory. Entered argument " 
              + arguments[1] 
              + " is not directory. Please check --help")

        return False
    
    elif ("-o" in arguments):

        # check if directory path after --o exists
        if (len(arguments) < arguments.index("-o") + 1):

            globals.show_message("Invalid argument for output directory. Output directory " +
                  "can't be empty")
            
            return False

        # check if entered output directory is directory
        elif (check_output_directory(arguments[arguments.index("-o") + 1]) == ""):

            globals.show_message("Invalid argument for output directory. Entered argument " 
                  + arguments[arguments.index("-o") + 1]
                  + " is not directory. Please check --help")

            return False

    return True

# it needs because cue2cu2 use modes for cu2 generation that depends of system
# console version
def check_menu_console_version() -> int:

    wrong_answer : bool = True

    while wrong_answer:

        globals.show_message('''
        For correct cu2 sheets you need to enter your PSIO menu system version \n
        1 - If your version less than 2.8 \n
        2 - If your system equal or more than 2.8 \n
                     ''')

        answer : str = str(input())
        

        if (not answer.isdigit()):
            globals.show_message("Entered string has letter. Enter the 1 or 2 in terminal")
            

        else:

            if(answer == "1" or answer == "2"):
                return int(answer)

            else:
                globals.show_message("Entered number is not 1 or 2. Enter the 1 or 2 in terminal")
                
def check_output_directory(path : str) -> str:

    if (os.path.isdir(path)):

        globals.show_message("Set output directory in " + str(os.path.abspath(path)))
        
        return path

    else:

        globals.show_message("No output directory inserted")
        

        return "" 


def create_output_directory():

    if (not "converted" in os.listdir("../")):

        os.mkdir("../converted")
        globals.show_message("Created output path " + 
                             str(os.path.abspath("../converted")))
    else:

        globals.show_message("Use output path " +  
                             str(os.path.abspath("../converted")))
        
def set_output_directory(arguments : list) -> str:

    if ("-o" in arguments):

        globals.show_message(arguments[arguments.index("-o") + 1])
        return arguments[arguments.index("-o") + 1]
    
    else:
        
        create_output_directory()
        return "../converted/"

# if user don't set output folder create it manually
def check_input_path(path : str) -> bool:

    if os.path.isdir(path):

        globals.show_message("Set input directory " + str(os.path.abspath(path)))
        
        return True

    else:

        globals.show_message("Inserted argument is not directory")
        

        return False

# function scan files in input folder and reterns dictionary that has file names
# as keys and values as count of bin files for every cue file 
def scan_files(input_directory : list) -> dict:

    cue_bin_files = {}

    for disc_file in input_directory:

        # for binmerge we need only file with .cue extension
        if disc_file.split('.')[-1] == 'cue':

            cue_bin_files[disc_file] = scan_bin_files(input_directory, disc_file) 

    return(cue_bin_files)

# scan .bin files that related to entered .cue file
def scan_bin_files(input_directory : list, disc_file: str) -> int:

    bin_files_count = 0

    for i in input_directory:
        
        if i.split('.')[-1] == 'bin' and disc_file.split(".cue")[0] in i:

            bin_files_count += 1

    return bin_files_count

def convert_files(cue_files : dict, 
                  input_directory : str,
                  output_directory : str,
                  format_mode : int):

    # cicle that parse all files in input directory and converting them
    for cue_file in cue_files:

        game_title : str = globals.extract_game_title(cue_file)
        file_output_directory : str = os.path.abspath(output_directory + "/" + game_title)
        check_file_output_directory(file_output_directory)

        # progarm won't work if .cue file don't have .bin file with the same name
        if cue_files[cue_file] == 0:

            globals.show_message(f"File {cue_file} do not have related .bin files. Skip")
            
            continue

        elif cue_files[cue_file] == 1:
            
            if (check_if_image_is_multidisc(cue_file)):

                move_files_to_output_directory(cue_file, input_directory, file_output_directory)

                globals.update_multidisc_file(file_output_directory)

            else:

                move_files_to_output_directory(cue_file, input_directory, file_output_directory)

        else:

            merge_bin_files(cue_file,
                            game_title,
                            input_directory, 
                            file_output_directory)
        

        if (check_cue_for_cd_audio(cue_file, file_output_directory)):

            make_cu2_file(
                    cue_file, 
                    file_output_directory,
                    format_mode)
        
    set_game_covers(os.path.abspath(output_directory))


# if output file directory does not exists create it
def check_file_output_directory(directory : str):

    if not (os.path.exists(directory)):

        globals.show_message(f"Create directory {directory}") 

        os.mkdir(directory)
        
    else:
        
        globals.show_message(f"Use {directory}")
        
def check_if_image_is_multidisc(cue_file : str) -> bool:

    return (re.search("(Disc [0-9])", cue_file) != None)


# if image don't splitted in .bin files it will be replace to it's output directory
def move_files_to_output_directory(cue_file :str, input_directory : str, output_directory : str):

        shutil.copy(os.path.abspath(input_directory + "/" + cue_file), 
                    output_directory)

        shutil.copy(os.path.abspath(input_directory + 
                                    "/" + cue_file.split(".cue")[0] + ".bin"), 
                                    output_directory + "/" +
                                    cue_file.split(".cue")[0] + ".bin")

# function that will execute binmerge
def merge_bin_files(cue_file : str, title : str, input_directory : str,  output_directory : str):

    binmerge_arguments = ["python3", 
                          "../binmerge/binmerge", 
                          input_directory + "/" + cue_file, 
                          cue_file.split(".cue")[0], 
                          "-o", 
                          output_directory]

    subprocess.run(binmerge_arguments)

    globals.show_message("File " + cue_file + " converted")


def check_cue_for_cd_audio(cue_file : str, file_directory : str) -> bool:


    with open(file_directory + "/" + cue_file, "r") as opened_file:

        content = opened_file.read()

        if ("AUDIO" in content):

            globals.show_message("CD audio detected, use CUE2CU2")
            
            return True
        
        return False

def make_cu2_file(cue_file : str, input_directory : str, format_mode : int):

    cue2cu2_argumets = ["python3",
                    "../cue2cu2/cue2cu2.py", 
                        os.path.abspath(input_directory) + "/" + cue_file, 
                        "-f", str(format_mode)]

    subprocess.run(cue2cu2_argumets)
    
def set_game_covers(output_directory : str):
    
    for i in os.listdir(os.path.abspath(output_directory)):

        file_directory = (output_directory + "/" + i)
        image_creator.find_image(i.split("(")[0], file_directory)
        
if __name__ == "__main__":
    main(sys.argv)
