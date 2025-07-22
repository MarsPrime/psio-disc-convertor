import re
import os

terminal_columns = os.get_terminal_size().columns
def show_message(text : str):

    print()
    print(terminal_columns* "#")
    print(text)
    print(terminal_columns* "#")
    print()

def show_dialog(text : str) -> bool:
    
    dialog_cicle : bool = True
    answer : str

    while (dialog_cicle):

        print()
        print(terminal_columns * "#")
        print(text)
        print("Enter y for YES or n for NO")
        print(terminal_columns * "#")

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
