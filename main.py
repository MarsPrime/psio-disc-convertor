import os
import sys
import subprocess

def main(arguments : list):

    if (not "converted" in os.listdir("./")):
        os.mkdir("./converted")

    disc_files : list = os.listdir(arguments[1])

    for disc_file in disc_files:
        if disc_file.split('.')[-1] == 'cue':

            subprocess.run(["python3",
                            "./binmerge/binmerge", 
                            arguments[1] + "/" + disc_file,
                            disc_file.split(".")[0], 
                            "-o", 
                            "./converted"])
           
        


if __name__ == "__main__":
    main(sys.argv)
