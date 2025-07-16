def show_message(text : str):

    print()
    print(20 * "#")
    print(text)
    print(20 * "#")
    print()

def show_dialog(text : str) -> bool:
    
    dialog_cicle : bool = True
    answer : str

    while (dialog_cicle):

        print()
        print(20 * "#")
        print(text)
        print(20 * "#")

        answer = input("Enter answer: ")

        print()

        if (answer == "y" or answer == "Y"):

            return True
        
        elif (answer == "n" or answer == "N"):

            return False

        else:
            
            continue

