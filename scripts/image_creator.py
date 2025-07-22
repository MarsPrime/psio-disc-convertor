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

    print(suggested_games)

    if suggested_games != []:

        game_in_list = select_game(suggested_games)

        if game_in_list != -1:

            game_id = suggested_games[game_in_list][1]
            
            cover_file = find_game_cover_by_id(game_id)

            if (cover_file != ""):

                create_game_cover_image(cover_file, output_directory) 
    
    else:

        globals.show_message("Program can't find games that has title like that")
        
        correct_answer : str = ""
        while (correct_answer == ""):

            globals.show_message(f'''Enter game title manually if you want to find game cover 
                                 for title: {game_title}
                                 If you don't want to do this just press enter''')

            answer : str = input()

            if answer == "":

                return

            else:
                find_image(answer, output_directory)
                return


def search_game_in_game_db(game_title : str) -> list:

        game_title = game_title.split(" - ")[0]


        if game_title[-1] == " ":
            game_title = game_title[:-1]

        connection : sql.Connection = sql.connect("../game_db_creator/GameDB")
        cursor : sql.Cursor = connection.cursor()
        
        print(game_title)
        cursor.execute('''
        SELECT GAME_TITLE, GAME_ID, LANGUAGES FROM Games WHERE GAME_TITLE LIKE(?);
        ''', ("%" + game_title + "%", ))

        found_games_list = cursor.fetchall()

        games_list = []

        for game in found_games_list:

            games_list.append([game[0].replace("\xa0", ""), game[1], game[2].replace("\xa0", "")])

        return games_list


def show_game_selection_dialog(game_list : list, count : int) -> list:

    globals.show_message("Selecting game cover")

    list_end : int

    if (len(game_list) < count + 10):

        list_end = len(game_list)

    else:

        list_end = count + 10

    for game in range(count, list_end):

        # I dont use function globals.show_message because I need to output table 
        print(str(game) + ")", "\t", game_list[game][1], "\t", game_list[game][0], "\t",
              game_list[game][2])


    globals.show_message("Select one game from list by typing it's number in console. "
         " If you want to go on previous page type p. "
         " If you want to go on next page print n.")

    return [str(input()), list_end]

def select_game(game_list : list) -> int:
    
    if len(game_list) == 1:

        return 0

    elif len(game_list) < 1:

        return -1

    game_number_in_list : int = -1

    page_count : int = 0

    while (game_number_in_list == -1):

        answer = (show_game_selection_dialog(game_list, page_count))

        if answer[0] == "n":

            if (page_count + 10 <= answer[1]):

                page_count += 10

            else:
                
                if (page_count < answer[1]):

                    page_count =  answer[1] - (answer[1] - page_count)

        elif answer[0] == "p":

            if (page_count - 10 >= 0):
                
                page_count -= 10

        else:
            if (answer[0].isdigit() and answer != ""):

                if (int(answer[0]) >= page_count and int(answer[0]) < answer[1]):

                    return int(answer[0])

                else:
                    
                    globals.show_message("Entered number is not in displayed list")

            else:

                globals.show_message("Enter number of game in list ")


        

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

