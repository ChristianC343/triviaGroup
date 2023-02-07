import random
import qanda

def startGame(numOfQues):
    game = qanda.Qanda()
    game.runGame(numOfQues)


def main():
    print("Hello, Welcome to a Quick Round of Trivia!")
    name = input("Please enter your name: ") # User Name
    progRunning = True #Will continue to keep the program running until user exit
    print("Welcome " + name + ", this is a prototype trivia game.")
    while progRunning == True:
        print("1. Show Leaderboard")
        print("2. Play Easy Mode (5 Questions)")
        print("3. Play Medium Mode (10 Questions)")
        print("4. Play Hard Mode (15 Questions)")
        print("5. Quit")
        selection = input("Please make a selection: ")
        selection = int(selection) # static cast string to int

        if selection == 1:
            print("Leaderboard")
        elif selection == 2:
            print("Easy Mode")
            startGame(5)
        elif selection == 3:
            print("Medium Mode")
            startGame(10)
        elif selection == 4:
            print("Hard Mode")
            startGame(15)
        elif selection == 5:
            print("Thanks for Playing!")
            progRunning = False
        else:
            print("Invalid Choice. Try again")

if __name__ == "__main__":
    main()