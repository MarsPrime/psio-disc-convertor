import re
import os
import time

from termcolor import colored, cprint

terminal_columns = os.get_terminal_size().columns
def show_message(text : str):

    print()
    cprint(terminal_columns * "#", "green")
    print(text)
    cprint(terminal_columns * "#", "green")
    print()

    time.sleep(1)

def show_dialog(text : str) -> bool:
    
    dialog_cicle : bool = True
    answer : str

    while (dialog_cicle):

        print()
        cprint(terminal_columns * "#", "yellow")
        print(text)
        cprint("Enter y for YES or n for NO", "red", attrs=["bold"])
        cprint(terminal_columns * "#", "yellow")

        answer = input("Enter answer: ")

        print()

        if (answer == "y" or answer == "Y"):

            return True
        
        elif (answer == "n" or answer == "N"):

            return False

        else:
            
            continue

def extract_game_title(cue_file : str) -> str:
    game_title = cue_file.split(".cue")[0]
    game_title = re.split(r" \(Disc [0-9]\)", game_title)[0]
    game_title = re.split(r"\(USA\)", game_title)[0]
    game_title = re.split(r"\(Europe\)", game_title)[0]
    game_title = re.split(r"\(Russia\)", game_title)[0]
    game_title = re.split(r"\(Europe.+?\)", game_title)[0]
    game_title = re.split(r"\(Japan\)", game_title)[0]
    
    if game_title[-1] == " ":
        game_title = game_title[:-1]

    return game_title
            
def update_multidisc_file(input_directory : str):

     
    with open(input_directory + "/MULTIDISC.LST", "w", encoding="cp1251") as multi_disc_file:
        
        for file in sorted(os.listdir(input_directory)):

            if ".bin" in file:

                multi_disc_file.write(file + "\r\n")

