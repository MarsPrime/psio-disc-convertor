import table_parser
import os
import sqlite3 as sql
from PIL import Image

def find_image(game_title : str, output_directory: str):
    
    if (os.path.exists("../game_db_creator/GameDB")):

        print("Found games DB")

    else:

        print("Games DB not found. Create new")

        table_parser.main()

        print("DB created")

    suggested_games = search_game_in_game_db(game_title)


    if suggested_games != []:

        game_in_list : int = select_game(suggested_games)

    else:

        return
    
    game_id = suggested_games[game_in_list][1]
    
    create_game_cover(game_id, output_directory)


def search_game_in_game_db(game_title : str) -> list:

        game_title = game_title.split(" - ")[0]
        
        if game_title[-1] == " ":
            game_title = game_title[:-1]

        connection : sql.Connection = sql.connect("../game_db_creator/GameDB")
        cursor : sql.Cursor = connection.cursor()
        
        cursor.execute('''
        SELECT GAME_TITLE, GAME_ID, LANGUAGES FROM Games WHERE GAME_TITLE LIKE(?);
        ''', ("%" + game_title + "%", ))



        founded_games = cursor.fetchall()

        games_list = []


        for game in founded_games:
            games_list.append([game[0].replace("\xa0", ""), game[1], game[2].replace("\xa0", "")])

        return games_list

def show_game_selection_dialog(game_list : list, count : int) -> str:

    print("#" * 20)
    for game in range(count, count + 10):

        print(str(game) + ")", "\t", game_list[game][1], "\t", game_list[game][0], "\t",
              game_list[game][2])


    print("#" * 20)
    print("Select one game from list by typing it's number in console. "
         " If you want to go on previous page type p. "
         " If you want to go on next page print n.")
    print("#" * 20)

    return str(input())

def select_game(game_list : list) -> int:
    
    correct_answer : int = -1 

    count = 0

    while (correct_answer == -1):

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

                        correct_answer = int(answer)

                    else:

                        print("Entered number is not in this list")

                        continue
                else:

                    continue

        return correct_answer
        
def create_game_cover(game_id : str, output_directory : str):

    for id in game_id.split(" "):
        convert_image(id, output_directory)
    

def convert_image(game_id : str, output_directory :str):
    game_covers_directory = "../game_covers/covers/default/"

    image_file = game_id + ".jpg"

    if (image_file in os.listdir(game_covers_directory)):
        
        print("Cover found")

        image = Image.open(game_covers_directory + image_file)
        
        resized_image = image.resize((80, 84))

        resized_image = resized_image.save(output_directory + "/cover.bmp")
        
    
    else:
        print("Cover don't found")


