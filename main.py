import random
import qanda
import leaderboard
import sys

def startGame(numOfQues):
    game = qanda.Qanda()
    return game.runGame(numOfQues)

def main():
    print("Hello, Welcome to a Quick Round of Trivia!")
    name = input("Please enter your name: ") # User Name
    progRunning = True #Will continue to keep the program running until user exit
    #checks if the users information exists or not to display different welcome message
    #leaderboard.readfile("leaderboard.txt")
    #existing_user = leaderboard.get_user(name)
    #if existing_user:
    #    print("Welcome back " + name + ", this is a prototype trivia game.")
    #else:
    
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
            score = startGame(5)
            #leaderboard.save_user(name, score)
        elif selection == 3:
            print("Medium Mode")
            score = startGame(10)
            #leaderboard.save_user(name, score)
        elif selection == 4:
            print("Hard Mode")
            score = startGame(15)
            #leaderboard.save_user(name, score)
        elif selection == 5:
            print("Thanks for Playing!")
            #leaderboard.writefile("leaderboard.txt")
            sys.exit()
        else:
            print("Invalid Choice. Try again")

if __name__ == "__main__":
    main() 
