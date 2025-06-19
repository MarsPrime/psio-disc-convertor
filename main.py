import os
import sys
import subprocess

def main(arguments : list):

    output_directory = ""
    if (not check_input_path(arguments)):
        print("Invalid argument. Please check --help")
        return
    
    # check if user set output path
    if ("-o" in arguments):

        output_directory = check_output_path(arguments[arguments.index("-o") + 1])

        if (output_directory == ""):
            print("Invalid argument. Please check --help")
            return
        else:
            print("Found output folder")

    else:

        create_output_path() 
        
        output_directory = "./converted/"
    
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
           
        
def create_output_path():

    if (not "converted" in os.listdir("./")):
        os.mkdir("./converted")


def check_input_path(arguments : list) -> bool:

    if os.path.isdir(arguments[1]):
        print("Found entered directory")
        # check if user set output  path
        return True

    else:
        print("Inserted argument is not folder")
        return False

def check_output_path(path : str) -> str:
    if (os.path.isdir(path)):
        return path
    else:
        return "" 

if __name__ == "__main__":
    main(sys.argv)
