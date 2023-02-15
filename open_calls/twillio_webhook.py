import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from os.path import exists
from things.actors import actor



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
next_prompt = None

with open('chatbot_corpus.json', 'r') as myfile: # open and read the json file
    CORPUS = json.loads(myfile.read())
with open('chatbot_trivia.json', 'r') as myfile: # open and read the json file
    TRIVIA = json.loads(myfile.read())


def handle_request():
    logger.debug(request.form)

    act = None
    if exists( f"users/{request.form['From']}.pkl") :
        with open(f"users/{request.form['From']}.pkl", 'rb') as p:
            act = pickle.load(p) 
    else:
        act= actor(request.form['From'])

    act.save_msg(request.form['Body'])
    logger.debug(act.prev_msgs)
    

    response = 'NOT FOUND'
    next_prompt = None
    sent_input = str(request.form['Body']).lower()# getting the input sent from the user, converting to lower
   
    if sent_input in CORPUS['input']: # check to see the if the sent input is inside the json file
        response = CORPUS['input'][sent_input]
    elif sent_input == 'trivia':
        response = TRIVIA['init']['content']
        next_prompt = TRIVIA['name_prompt']['content']    
    elif 'name' not in act.state:
        act.state['name'] = sent_input  # set the user's name to the state attribute
        response = TRIVIA['welcome_message']['content'].format(name=sent_input)
        next_prompt = TRIVIA['selection_prompt']['content'] + '\n' + '\n'.join(TRIVIA['menu_options'])
        
    else:
        CORPUS['input'][sent_input] = ['DID NOT FIND']
        with open('chatbot_corpus.json', 'w') as myfile:
            myfile.write(json.dumps(CORPUS, indent=4 ))

    logger.debug(response)

    message = g.sms_client.messages.create(
                     body=response,
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])

    message = g.sms_client.messages.create(
                     body=next_prompt,
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])
    

    
    return json_response( status = "ok" )

