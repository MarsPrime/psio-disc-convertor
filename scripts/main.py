import os
import sys
import subprocess
import shutil

import image_creator

def main(arguments : list):

    if (not check_arguments_validity(arguments)):
        return

    # set ouput directory
    output_directory = set_output_directory(arguments)

    # select path of disc images
    input_directory_files: list = os.listdir(arguments[1])

    cue_files = scan_files(sorted(input_directory_files))


    for cue_file in cue_files:
         
        show_message(cue_file)

        if cue_files[cue_file] > 1:

             merge_bin_files(cue_file, arguments[1], output_directory)

        elif ("(Disc" in cue_file):
            
            move_multi_disc_files(cue_file, arguments[1], output_directory)

        else:

            if not os.path.exists(os.path.abspath(output_directory + "/" + cue_file.split(".cue")[0])):

                os.mkdir(os.path.abspath(output_directory + "/" + cue_file.split(".cue")[0]))

            move_files_to_output_directory(cue_file, arguments[1],
                                           os.path.abspath(output_directory + "/" + cue_file.split(".cue")[0]))
            

        if (check_cue_for_cd_audio(cue_file, output_directory)):

            make_cu2_file(cue_file, output_directory + "/" + cue_file.split(".cue")[0].split("(Disc")[0])
        

    
    set_game_covers(os.path.abspath(output_directory))
        #image_creator.find_image(output_directory, output_directory)
        

# function scan files in input folder and reterns dictionary that has file names
# as keys and values as count of bin files for every cue file 
def scan_files(input_directory : list) -> dict:

    cue_bin_files = {}

    for disc_file in input_directory:

        # for binmerge we need only file with .cue extension
        if disc_file.split('.')[-1] == 'cue':

            cue_bin_files[disc_file] = scan_bin_files(input_directory, disc_file) 

    return(cue_bin_files)

def scan_bin_files(input_directory : list, disc_file: str) -> int:

    bin_files_count = 0

    for i in input_directory:
        
        if i.split('.')[-1] == 'bin' and disc_file.split(".cue")[0] in i:

            bin_files_count += 1

    return bin_files_count

# function that will execute binmerge
def merge_bin_files(cue_file : str, input_directory : str,  output_directory : str):

    disc_path = output_directory + "/" + cue_file.split(".")[0]

    if (not delete_converted_files(cue_file, disc_path)):

        return 

    else:

        if (not os.path.exists(output_directory + "/" + cue_file.split(".")[0])):
            os.mkdir(output_directory + "/" + cue_file.split(".")[0])


        binmerge_arguments = ["python3",
                        "../binmerge/binmerge", 
                        input_directory + "/" + cue_file,
                        cue_file.split(".")[0], 
                              "-o"]

        binmerge_arguments.append(disc_path)

        subprocess.run(binmerge_arguments)

        show_message("File " + cue_file + " converted")

# function move multi disc games to one folder and create file MULTIDISC.LST
def move_multi_disc_files(cue_file : str, input_directory : str, output_directory : str):

    multi_disc_directory = os.path.abspath(output_directory + "/" 
                                           + cue_file.split("(Disc")[0])

    if (os.path.exists(multi_disc_directory)):

        show_message("File " + cue_file + 
                     " moved to directory " + multi_disc_directory)

        move_files_to_output_directory(cue_file, input_directory, multi_disc_directory)

    else:

        show_message("path for file " + multi_disc_directory + " wont found, create directory")

        os.mkdir(multi_disc_directory)

        show_message("move file " + cue_file  + " to new directory")

        move_files_to_output_directory(cue_file, input_directory, multi_disc_directory)


    show_message("File MULTIDISC.LST found. Update it")

    update_multidisc_file(multi_disc_directory)

def move_files_to_output_directory(cue_file :str, input_directory : str, output_directory : str):

        shutil.copy(os.path.abspath(input_directory + "/" + cue_file), 
                    output_directory)

        shutil.copy(os.path.abspath(input_directory + 
                                    "/" + cue_file.split(".cue")[0] + ".bin"), 
                                    output_directory + "/" +
                                    cue_file.split(".cue")[0] + ".bin")

def check_multi_disc_file(input_directory : str) -> bool:

    return os.path.exists(input_directory + "/MULTIDISC.LST")

def update_multidisc_file(input_directory : str):
    
    with open(input_directory + "/MULTIDISC.LST", "w") as multi_disc_file:
        
        for file in sorted(os.listdir(input_directory)):

            if ".bin" in file:

                multi_disc_file.write(file + "\n")

            
def check_cue_for_cd_audio(cue_file : str, input_directory : str) -> bool:

    cue_file_directory : str = (os.path.abspath(input_directory) + 
                                "/" + cue_file.split(".cue")[0].split("(Disc")[0] + 
                                "/" + cue_file)
   

    with open(cue_file_directory, "r") as opened_file:

        content = opened_file.read()

        if ("AUDIO" in content):

            show_message("CD audio detected, use CUE2CU2")
            
            return True
        
        return False


def make_cu2_file(cue_file : str, input_directory : str):
    cue2cu2_argumets = ["python3",
                    "../cue2cu2/cue2cu2.py", 
                        os.path.abspath(input_directory) + "/" + cue_file]
    show_message(input_directory + "/" + cue_file)
    subprocess.run(cue2cu2_argumets)
    




# if user don't set output folder create it manually
def check_input_path(path : str) -> bool:

    if os.path.isdir(path):

        show_message("Set input directory " + str(os.path.abspath(path)))

        return True

    else:

        show_message("Inserted argument is not directory")

        return False


def check_output_directory(path : str) -> str:

    if (os.path.isdir(path)):

        show_message("Set output directory in " + str(os.path.abspath(path)))

        return path

    else:

        show_message("No output directory inserted")

        return "" 


def create_output_directory():

    if (not "converted" in os.listdir("../")):

        os.mkdir("../converted")
        show_message("Created output path " + str(os.path.abspath("../converted")))

    else:

        show_message("Use output path " +  str(os.path.abspath("..//converted")))


def set_output_directory(arguments : list) -> str:

    if ("-o" in arguments):

        show_message(arguments[arguments.index("-o") + 1])
        return arguments[arguments.index("-o") + 1]
    
    else:
        
        create_output_directory()
        return "../converted/"

# check all given arguments
def check_arguments_validity(arguments : list) -> bool: 

    if (not check_input_path(arguments[1])):

        show_message("Invalid argument for input directory. Entered argument " 
              + arguments[1] 
              + " is not directory. Please check --help")

        return False
    
    elif ("-o" in arguments):

        # check if directory path after --o exists
        if (len(arguments) < arguments.index("-o") + 1):

            show_message("Invalid argument for output directory. Output directory " +
                  "can't be empty")
            
            return False

        # check if entered output directory is directory
        elif (check_output_directory(arguments[arguments.index("-o") + 1]) == ""):

            show_message("Invalid argument for output directory. Entered argument " 
                  + arguments[arguments.index("-o") + 1]
                  + " is not directory. Please check --help")

            return False


    return True

def delete_converted_files(disc_file : str, output_directory : str) -> bool:

    if (check_converted_file_existence(os.path.abspath(output_directory) + 
                                       "/" +
                                       disc_file)):
        message : str = "Program detects converted files in output path "
        message += "for file " + disc_file.split(".")[0] + "."
        message += " Delete this files? Enter y for YES or n for NO "

        if (not show_dialog(message)):

            show_message("User abort operation. Close.")
            
            return False

        else:
            
            show_message("Delete converted files")

            os.remove(os.path.abspath(output_directory) + "/" + disc_file)
            os.remove(os.path.abspath(output_directory) + "/" 
                      + disc_file.split(".")[0] + ".bin")

            return True

    return True



def check_converted_file_existence(output_path : str) -> bool:

    if os.path.exists(output_path):

        return True
    
    else:

        return False

def set_game_covers(output_directory : str):
    print(os.path.abspath(output_directory))
    
    
    for i in os.listdir(os.path.abspath(output_directory)):

        file_directory = (output_directory + "/" + i)
        image_creator.find_image(i.split("(")[0], file_directory)
        
def show_message(text : str):

    print()
    print(20 * "#")
    print(text)
    print(20 * "#")
    print()

def show_dialog(text : str) -> bool:
    
    dialog_cicle : bool = True
    answer : str

    while (dialog_cicle):

        print()
        print(20 * "#")
        print(text)
        print(20 * "#")

        answer = input("Enter answer: ")

        print()

        if (answer == "y" or answer == "Y"):

            return True
        
        elif (answer == "n" or answer == "N"):

            return False

        else:
            
            continue
        

if __name__ == "__main__":
    main(sys.argv)
