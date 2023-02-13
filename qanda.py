import random


# idea: takes question and answer from an input file, randomly selects one pair
# and puts into a tuple
class Qanda:  # class for questions and answers
    string1 = "qanda created"
    qlist = []
    alist = []
    score = 0

    def __init__(self):
        # when a new object is defined, creates a question and answer stored into 2 lists, along with dummy answers
        with open("q&a") as file: #open and read q&a file
            counter = 1
            for line in file:
                if line == "":
                    break
                elif counter % 2 == 0:  # start at line 1. If line is odd, it is a question. If even, it is an answer
                    self.alist.append(line)
                    counter += 1
                else:
                    self.qlist.append(line)
                    counter += 1

    def printQuestions(self):
        for x in self.qlist:
            print(x)

    def printAnswers(self):
        for x in self.alist:
            print(x)

    def runGame(self, questions):
        counter = questions
        used = []  # a list of questions that were already used
        while counter > 0:
            validQuestion = True
            randNum = random.randint(0, (len(self.qlist) - 1)) #random number is between 0 and length of list
            exist_count = used.count(randNum) # check to see if the question has been used
            if exist_count > 0: #if the number is found in the used list
                randNum = random.randint(0, (len(self.qlist) - 1)) # generate a new random number
                validQuestion = False
                exist_count = 0 #reset exist number counter

            if validQuestion:
                print("Question: " + self.qlist[randNum])
                answers = self.alist[randNum]
                answers = answers.split(",") #split answers up into an answer list
                a = answers[0] # first index is the right answer
                b = answers[1]
                c = answers[2]
                d = answers[3]
                print("A. "+a)
                print("B. "+b)
                print("C. "+c)
                print("D. "+d)
                userAnswer = input("Answer: ")
                if userAnswer.upper() == "A": #as of right now, A is the only correct answer
                    self.score += 1
                    print("Correct!")
                else:
                    print("Wrong!")

                used.append(randNum)
                counter -= 1
                
        print('\n', "Your Final score is: ", self.score, '\n') 
        return self.score

        



