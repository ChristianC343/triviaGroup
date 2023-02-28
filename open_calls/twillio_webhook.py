
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

questions_answered = [-1]

def leaderboard_info_entered(user_id, act):
    
    last_response = act.prev_msgs[-1]

    LEADERBOARD = {}

    with open('chatbot_leaderboard.json', 'r') as leaderboardFile: 
        LEADERBOARD = json.loads(leaderboardFile.read())
    
    LEADERBOARD.append({
        'Name': last_response[5:],
        'Score': CORPUS[user_id]['current_game']['score']
    })

    with open('chatbot_leaderboard.json', 'w') as leaderboardFile:
            json.dumps(LEADERBOARD, leaderboardFile, indent=4,  separators=(',',': '))



    CORPUS[user_id]['current_game']['score']


def start_game(user_id, response):
    questions = TRIVIA['questions']
    random_index = -1
    while random_index in questions_answered:
        random_index = random.randint(0, len(questions)-1)
    
    selected_question = questions[random_index]['question']

    options = list(questions[random_index]['options'].values())
    answer = questions[random_index]['answer']
    question_text = f"Question : {selected_question}\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}\nEnter your answer (A, B, C, or D):"
    # Initialize the user's CORPUS if it doesn't exist
    if user_id not in CORPUS:
        CORPUS[user_id] = {}

    # Store the selected question for later reference

    CORPUS[user_id]['current_question'] = {'question': selected_question, 'answer': answer}
    
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
    questions_answered.append(random_index)
    print(questions_answered)

    #response = ''




def handle_request():
    logger.debug(request.form)

    # Load or create user object
    act = None
    user_id = request.form['From']
    # filename = f"users/{user_id}.pkl"
    # os.makedirs("users", exist_ok=True)

    # if exists(filename):
    #     with open(f"users/{user_id}.pkl", 'rb') as p:
    #         act = pickle.load(p)
    #     print("I AM CURRENTLY LOADING")
    # else:
    #     act= actor(request.form['From'])
    #     # create the file and write the actor object to it
    #     with open(filename, "wb") as f:
    #         pickle.dump(actor, f)
    # 
    # print("Printing msg : " + msg)
    msg = request.form['Body']
    act = actor(user_id)
    act.save_msg(msg)
    last_response = act.prev_msgs[-1]
    logger.debug(act.prev_msgs)

    # Response strings
    hello_prompt = 'Hello, welcome to a quick round of trivia!'
    select = TRIVIA['selection_prompt']['content']
    lb = 'Leaderboard'
    easy = 'Easy mode'
    bye = 'Thanks for playing!'
    invalid = 'Invalid input. Please enter a valid option.'

    # Handle user input
    input_text = str(request.form['Body']).lower()

    # provide the menu options
    if last_response == 'Hello':
        response = hello_prompt + '\n' + select + '\n'+ '\n'.join(TRIVIA['menu_options'])
        
   
    # display the leaderboard
    elif last_response == '1':
        response = "UNDER CONSTRUCTION! " + '\n' + "Text 'Hello' for the menu options"
    
    # start a round of easy mode trivia
    elif last_response == str(2):
        begin = 'Lets start the game!'
        start_game(user_id, begin)
        CORPUS[user_id]["current_game"] = {"question_num": 0, "score": 0}
    elif last_response == CORPUS[user_id]['current_question']['answer'] :
        #act.update_score(True)
        if CORPUS[user_id]['current_game']['question_num'] == 5:
            CORPUS[user_id]['current_game']['score'] +=1
            message = g.sms_client.messages.create(
            body="Enter a name after typing 'leadb'\nEX: leadb Name",
            from_=yml_configs['twillio']['phone_number'],
            to=request.form['From']
        )
            response = 'Correct!' + '\n' + 'Your final score is ' + str(CORPUS[user_id]['current_game']['score']) + '\n' + bye
        else:
            CORPUS[user_id]['current_game']['question_num'] +=1 
            CORPUS[user_id]['current_game']['score'] +=1
            correct = 'Correct! ' +'\n' + 'Your current score is ' + str(CORPUS[user_id]['current_game']['score']) 
            start_game(user_id, correct)
        
            
    elif last_response == 'B' or last_response == 'C' or last_response == 'D':
        #act.update_score(False)
        
        if  CORPUS[user_id]['current_game']['question_num'] == 5:
            response = 'Your final score is ' + str(CORPUS[user_id]['current_game']['score']) + '\n' + bye
        else:
            CORPUS[user_id]['current_game']['question_num'] +=1 
            incorrect = 'Incorrect! ' + '\n' + 'Your current score is ' + str(CORPUS[user_id]['current_game']['score'])
            start_game(user_id, incorrect)

    elif 'leadb' in last_response:
        leaderboard_info_entered(user_id, act)


            
    # If the user selects option 3, end the session and save the actor object
    elif last_response == '3':
        response = bye
        with open(f"users/{user_id}.pkl", 'wb') as f:
            pickle.dump(act, f)
    
    # If the user input is invalid, prompt them to enter a valid option
    else:
        response = invalid
        
    
    
    if response:
        message = g.sms_client.messages.create(
            body=response,
            from_=yml_configs['twillio']['phone_number'],
            to=request.form['From']
        )
    else:
        message = g.sms_client.messages.create(
            body="Sorry, we encountered an error. Please try again later.",
            from_=yml_configs['twillio']['phone_number'],
            to=request.form['From']
        )

    # Send the response back to the user
    
    logger.debug(response)
    
    return json_response(status="ok")


            
  

    
    return json_response( status = "ok" )

