import os
import sys
import subprocess


def main(arguments : list):

    if (not check_arguments_validity(arguments)):
        return

    # set ouput directory
    output_directory = set_output_directory(arguments)

    # select path of disc images
    disc_files : list = os.listdir(arguments[1])

    for disc_file in disc_files:

        # for binmerge we need only file with .cue extension
        if disc_file.split('.')[-1] == 'cue':

            disc_path = output_directory + "/" + disc_file.split(".")[0]

            if (not delete_converted_files(disc_file, disc_path)):

                continue

            else:

                if (not os.path.exists(output_directory + "/" + disc_file.split(".")[0])):
                    os.mkdir(output_directory + "/" + disc_file.split(".")[0])


                binmerge_arguments = ["python3",
                                "./binmerge/binmerge", 
                                arguments[1] + "/" + disc_file,
                                disc_file.split(".")[0], 
                                      "-o"]

                binmerge_arguments.append(disc_path)

                subprocess.run(binmerge_arguments)
                

                cue2cu2_argumets = ["python3",
                                "./cue2cu2/cue2cu2.py", 
                         os.path.abspath(output_directory) + "/" + disc_file.split(".")[0]+ "/" + disc_file]
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

    if (not "converted" in os.listdir("./")):

        os.mkdir("./converted")
        show_message("Created output path " + str(os.path.abspath("./converted")))

    else:

        show_message("Use output path " +  str(os.path.abspath("./converted")))


def set_output_directory(arguments : list) -> str:

    if ("-o" in arguments):

        show_message(arguments[arguments.index("-o") + 1])
        return arguments[arguments.index("-o") + 1]
    
    else:
        
        create_output_directory()
        return "./converted/"

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

        if (answer == "y"):

            return True
        
        elif (answer == "n"):

            return False

        else:
            
            continue
        
        

if __name__ == "__main__":
    main(sys.argv)
