import os
from bs4 import BeautifulSoup as bs
import numpy


def main():

    data_files : list = select_data_files()

    for file in data_files:

        parse_data(file)

def select_data_files() -> list:

    detected_files : list = []

    for file in os.listdir("./"):

        if ".html" in file:

            detected_files.append(file)

    return detected_files

def parse_data(file : str):

        soup = bs(open("./" + file, encoding="cp1252"), "html.parser")
        
        tables = soup.find_all("td")

        game_data = ""

        with open("./game_list.txt", "w+") as output_file:

            for i in range(len(tables)):
                if (i == 0):
                    continue

                if (i % 4 == 0 ):

                    output_file.write("\n")

                else:

                    output_file.write(tables[i].get_text(separator=" ").replace("\n", "") + "\t")


if __name__ == "__main__":
    main()
