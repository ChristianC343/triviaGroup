
import os
import time
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



yml_configs = {}
BODY_MSGS = []
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

CORPUS = {}
TRIVIA = {}


with open('chatbot_corpus.json', 'r') as myfile: 
    CORPUS = json.loads(myfile.read())
with open('chatbot_trivia.json', 'r') as myfile: 
    TRIVIA = json.loads(myfile.read())


import time


response = ''



def start_game(user_id, response):
    questions = TRIVIA['questions']
    random_index = random.randint(0, len(questions)-1)
    selected_question = questions[random_index]

    options = list(selected_question['options'].values())
    answer = selected_question['answer']
    question_text = f"Question : {selected_question['question']}\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}\nEnter your answer (A, B, C, or D):"
    # Initialize the user's CORPUS if it doesn't exist
    if user_id not in CORPUS:
        CORPUS[user_id] = {}

    # Store the selected question for later reference
    
    CORPUS[user_id]['current_question'] = {'question': selected_question['question'], 'answer': answer}
    
    with open('chatbot_corpus.json', 'w') as myfile:
            myfile.write(json.dumps(CORPUS, indent=4, default=list))
    message = g.sms_client.messages.create(
        to=user_id,
        from_=request.form['To'],
        body= response 
    )
    message = g.sms_client.messages.create(
        to=user_id,
        from_=request.form['To'],
        body= question_text
    )
    

    #response = ''




def handle_request():
    logger.debug(request.form)

    # Load or create user object
    act = None
    user_id = request.form['From']
    filename = f"users/{user_id}.pkl"
    os.makedirs("users", exist_ok=True)

    if exists(filename):
        with open(f"users/{user_id}.pkl", 'rb') as p:
            act = pickle.load(p)
        print("I AM CURRENTLY LOADING")
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
    
    if next_prompt:
        message = g.sms_client.messages.create(
                         body=next_prompt,
                         from_=yml_configs['twillio']['phone_number'],
                         to=request.form['From'])
    
    return json_response( status = "ok" )
