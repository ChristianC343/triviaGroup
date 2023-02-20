
import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from os.path import exists




from tools.logging import logger
from things.actors import actor



import random
import json
import pickle
import qanda

class actor:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.prev_msgs = []
        self.state = {"init_flag": True}  # initialize the state dictionary with the "init_flag" variable set to True
        self.waiting = False

    def save_msg(self, msg):
        self.prev_msgs.append(msg)





yml_configs = {}
BODY_MSGS = []
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

CORPUS = {}
TRIVIA = {}


with open('chatbot_corpus.json', 'r') as myfile: # open and read the json file
    CORPUS = json.loads(myfile.read())
with open('chatbot_trivia.json', 'r') as myfile: # open and read the json file
    TRIVIA = json.loads(myfile.read())


def startGame(numOfQues):
    game = qanda.Qanda()
    with open("q&a") as file: #open and read q&a file
            counter = 1
            for line in file:
                if line == "":
                    break
                elif counter % 2 == 0:  # start at line 1. If line is odd, it is a question. If even, it is an answer
                    game.alist.append(line)
                    counter += 1
                else:
                    game.qlist.append(line)
                    counter += 1
    response = "Let's start the game!\n"
    for i in range(numOfQues):
        q = game.qlist[i]
        a = game.alist[i].split(",")
        response += f"\nQuestion {i+1}: {q}"
        rndmz = random.sample(range(0, 3) 4)
        response += f"\nA. {a[rndmz[0]]}"
        response += f"\nB. {a[rndmz[1]]}"
        response += f"\nC. {a[rndmz[2]]}"
        response += f"\nD. {a[rndmz[3]]}"
    response += "\n\nPlease respond with your answers as A, B, C, or D."
    message = g.sms_client.messages.create(
        body=response,
        from_=yml_configs['twillio']['phone_number'],
        to=request.form['From']
    )
    return ""



def handle_request():
    logger.debug(request.form)

    #act = actor(request.form['From'])

    hello_prompt = 'Hello, Welcome to a Quick Round of Trivia!'
    select = TRIVIA['selection_prompt']['content']
    lb = 'Leaderboard'
    easy = 'Easy Mode'
    bye = 'Thanks for Playing!'

    sent_input.lower() = str(request.form['Body'])

    if sent_input == 'hello': 
        response = hello_prompt + '\n' + select + '\n'+ '\n'.join(TRIVIA['menu_options'])
    else:
        if sent_input in ['1', '2', '3']:
            if sent_input == '1':
                response = lb
            elif sent_input == '2':
                response = easy
                startGame(5)
            elif sent_input == '3':
                response = bye
                #progRunning = False
        else:
            response = 'Invalid input.'
    
    message = g.sms_client.messages.create(
            body=response,
            from_=yml_configs['twillio']['phone_number'],
            to=request.form['From'])

    logger.debug(response)

    return json_response(status="ok")
