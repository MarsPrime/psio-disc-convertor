import re
import os
from bs4 import BeautifulSoup as bs
import sqlite3 as sql


def main():

    data_files : list = select_data_files()

    for file in data_files:

        parse_data(file)

    insert_data_in_db("../game_db_creator/game_list.txt")

def select_data_files() -> list:

    detected_files : list = []

    if os.path.exists("../game_db_creator/game_list.txt"):

        os.remove("../game_db_creator/game_list.txt")

    for file in os.listdir("../game_db_creator"):

        if ".html" in file:

            detected_files.append(file)

    return detected_files

def parse_data(file : str):

        soup = bs(open("../game_db_creator/" + file, encoding="cp1252"), "html.parser")
        
        tables = soup.find_all("td")

        with open("../game_db_creator/game_list.txt", "a") as output_file:

            for i in range(len(tables)):
                if (i == 0):
                    continue

                if (i % 4 == 0 ):

                    output_file.write("\n")

                else:
                    data = tables[i].get_text(separator=" ").replace("\xa0", "")
                    data = tables[i].get_text(separator=" ").replace("\n", "")
                    data = data.split(" - ")[0].split("  -  ")[0]
                    data = data.split(" [ 2")[0].split((" [2"))[0]

                    data =  "".join(re.split("-*[0-9] DISCS*", data))
                    
                    data = data.replace("[ ]", "")

                    data += "\t"

                    
                    print(data)

                    output_file.write(data)


def insert_data_in_db(file : str):

    connection = sql.connect("../game_db_creator/GameDB")
    
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT exists Games (
    GAME_ID TEXT NOT NULL,
    GAME_TITLE TEXT NOT NULL,
    LANGUAGES TEXT NOT NULL);
    ''')

    connection.commit()


    with open(file, "r") as game_list:
        
        for i in game_list.readlines():

            game_code = i.replace("\n", "").split("\t")[0]
            game_title = i.replace("\n", "").split("\t")[1]
            game_languages = i.replace("\n", "").split("\t")[2]
            
            

            cursor.execute('''
            INSERT INTO Games(GAME_ID, GAME_TITLE, LANGUAGES) VALUES (?, ?, ?);
            ''', (game_code, game_title, game_languages))

            connection.commit()


if __name__ == "__main__":
    main()
