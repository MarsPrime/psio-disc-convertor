import globals # file with all global functions
import table_parser # file with table parser script for situation when GameDB don't created

import os
import sqlite3 as sql
from PIL import Image

def find_image(game_title : str, output_directory: str):
    
    if (os.path.exists("../game_db_creator/GameDB")):

        globals.show_message("Found games DB")

    else:

        globals.show_message("Games DB not found. Create new")

        # create games DB if it is don't detected
        table_parser.main()

        globals.show_message("DB created")


    suggested_games = search_game_in_game_db(game_title)


    if suggested_games != []:


        game_in_list = select_game(suggested_games)

        if game_in_list != -1:

            game_id = suggested_games[game_in_list][1]
            
            cover_file = find_game_cover_by_id(game_id)

            if (cover_file != ""):

                create_game_cover_image(cover_file, output_directory) 
    
    else:

        globals.show_message("Program can't find games that has title like that")
        return

def search_game_in_game_db(game_title : str) -> list:

        game_title = game_title.split(" - ")[0]


        if game_title[-1] == " ":
            game_title = game_title[:-1]

        connection : sql.Connection = sql.connect("../game_db_creator/GameDB")
        cursor : sql.Cursor = connection.cursor()
        
        cursor.execute('''
        SELECT GAME_TITLE, GAME_ID, LANGUAGES FROM Games WHERE GAME_TITLE LIKE(?);
        ''', ("%" + game_title + "%", ))

        found_games_list = cursor.fetchall()

        games_list = []

        for game in found_games_list:

            games_list.append([game[0].replace("\xa0", ""), game[1], game[2].replace("\xa0", "")])

        return games_list


def show_game_selection_dialog(game_list : list, count : int) -> str:

    print("#" * 20)

    list_end : int

    if (len(game_list) < count + 10):

        list_end = len(game_list)

    else:
        list_end = count + 10

    globals.show_message(str(list_end))

    for game in range(count, list_end):

        # I dont use function globals.show_message because I need to output table 
        print(str(game) + ")", "\t", game_list[game][1], "\t", game_list[game][0], "\t",
              game_list[game][2])


    globals.show_message("Select one game from list by typing it's number in console. "
         " If you want to go on previous page type p. "
         " If you want to go on next page print n.")

    return str(input())

def select_game(game_list : list) -> int:
    
    if len(game_list) == 1:

        return 0

    elif len(game_list) < 1:

        return -1
    
    game_order_number: int = -1 

    count = 0

    while (game_order_number == -1):

        answer = show_game_selection_dialog(game_list, count)

        match answer:

            case "n":

                if (count + 20 < len(game_list)):

                    count += 10

                else:

                    count = len(game_list) - 10

                continue

            case "p":

                if (count - 10 >= 0):
                    count -= 10

                else:
                    count = 0

                continue

            case _:

                if (answer.isdigit() and answer != ""):

                    if (int(answer) >= count and int(answer) < count + 10):

                        game_order_number = int(answer)

                    else:

                        globals.show_message("Entered number is not in this list")

                        continue
                else:

                    globals.show_message("Entered character not number or 'n' or 'r'")

                    continue

        return game_order_number 
        

def find_game_cover_by_id(game_id : str) -> str:

    for id in game_id.split(" "):

        print(id)
        if (id + ".jpg" in os.listdir("../game_covers/covers/default/")):

            globals.show_message("Cover found")


            return id + ".jpg" 
    
    globals.show_message("Cover don't found for game " + game_id)

    return ""
    

def create_game_cover_image(cover_file : str, output_directory : str):

    game_covers_directory = "../game_covers/covers/default/"

    default_cover_file = Image.open(game_covers_directory + cover_file)

    converted_cover_file = default_cover_file.resize((80, 84))
    
    converted_cover_file.save(output_directory + "/cover.bmp")





