import os
import sys
import subprocess


def main(arguments : list):

    print(check_arguments_validity(arguments))
    
    if (not check_arguments_validity(arguments)):
        return

    output_directory = set_output_path(arguments)

    print(output_directory)
    # select path of disc images
    disc_files : list = os.listdir(arguments[1])

    for disc_file in disc_files:

        # for binmerge we need only file with .cue extension
        if disc_file.split('.')[-1] == 'cue':

            binmerge_arguments = ["python3",
                            "./binmerge/binmerge", 
                            arguments[1] + "/" + disc_file,
                            disc_file.split(".")[0], 
                                  "-o"]

            binmerge_arguments.append(output_directory)

            subprocess.run(binmerge_arguments)
           
# if user don't set output folder create it manually
def check_input_path(path : str) -> bool:

    if os.path.isdir(path):

        print("Set input directory " + str(os.path.abspath(path)))

        return True

    else:

        print("Inserted argument is not directory")

        return False


def check_output_path(path : str) -> str:

    if (os.path.isdir(path)):

        print("Set output directory in " + str(os.path.abspath(path)))

        return path

    else:

        print("No output directory inserted")

        return "" 


def create_output_path():

    if (not "converted" in os.listdir("./")):

        os.mkdir("./converted")
        print("Created output path " + str(os.path.abspath("./converted")))

    else:

        print("Use output path " +  str(os.path.abspath("./converted")))


def set_output_path(arguments : list) -> str:
    if ("-o" in arguments):

        print(arguments[arguments.index("-o") + 1])
        return arguments[arguments.index("-o") + 1]
    
    else:
        
        create_output_path()
        return "./converted/"

# check all given arguments
def check_arguments_validity(arguments : list) -> bool: 

    if (not check_input_path(arguments[1])):

        print("Invalid argument for input directory. Entered argument " 
              + arguments[1] 
              + " is not directory. Please check --help")

        return False
    
    elif ("-o" in arguments):

        # check if directory path after --o exists
        if (len(arguments) < arguments.index("-o") + 1):
            print("Invalid argument for output directory. Output directory " +
                  "can't be empty")
            
            return False

        # check if entered output directory is directory
        elif (check_output_path(arguments[arguments.index("-o") + 1]) == ""):

            print("Invalid argument for output directory. Entered argument " 
                  + arguments[arguments.index("-o") + 1]
                  + " is not directory. Please check --help")

            return False


    return True


if __name__ == "__main__":
    main(sys.argv)
