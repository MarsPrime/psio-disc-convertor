import table_parser
import os
import sqlite3 as sql
import PIL

def find_image(game_title : str, output_folder : str):
    if (os.path.exists("../game_db_creator/GameDB")):

        print("Found games DB")

        connection : sql.Connection = sql.connect("../game_db_creator/GameDB")
        cursor : sql.Cursor = connection.cursor()
        
        cursor.execute('''
        SELECT Game_TITLE, GAME_ID, LANGUAGES FROM Games WHERE GAME_TITLE LIKE(?);
        ''', ("%" + game_title + "%", ))

        founded_games = cursor.fetchall()

        games_list = []

        for game in founded_games:
            games_list.append([game[0].replace("\xa0", ""), game[1], game[2].replace("\xa0", "")])

        for i in games_list:
            print(i)

    else:

        print("Games DB not found. Create new")

        table_parser.main()

        print("DB created")


find_image(input(), input())

