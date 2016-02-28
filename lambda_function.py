"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import json
import requests
import wolframalpha
import cloudconvert # pip install cloudconvert
#import re
#message_string = ""
#note_type = ""

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Un  comment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "InitialAskIntent":
        return initial_ask_intent(intent, session)
    elif intent_name == "NoteIntent":
        return note_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "WolframIntent":
        return wolfram_intent(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Note Taker Module. " \
                    "Please tell me what type of note you would like me to take. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what type of note you would like me to take. " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def initial_ask_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    reprompt_text = ""
    should_end_session = False
    
    if 'Notet' in intent['slots']:
        
        if 'value' in intent['slots']['Notet']:
            
            input_choice = intent['slots']['Notet']['value']
            
            if (input_choice == "picture"):
                speech_output = "Pictures are not currently supported. "
                reprompt_text = "Pictures are not currently supported. "
                should_end_session = True;
            else:
                speech_output = "What do you want your note to say? " 
                note_type = "string"
        else :
            speech_output = "I didn't quite hear that. " 
            reprompt_text = "Sorry, what was that? "
        
    else:
        speech_output = "I didn't quite hear that. " 
        reprompt_text = "Sorry, what was that? "
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
    """    
    session_attributes = {}
    should_end_session = False

    
    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    """                    
    
        
    


#def create_favorite_color_attributes(favorite_color):
#    return {"favoriteColor": favorite_color}


def note_intent(intent, session):
    
    session_attributes = {}
    reprompt_text = ""

    should_end_session = True

    
    if 'Note' in intent['slots']:
        if 'value' in intent['slots']['Note']:
            
            inputted_note = intent['slots']['Note']['value']
            message_string = inputted_note
            speech_output = "Ok, I am pushing your message, {}".format(inputted_note)
            reprompt_text = "Ok, I am pushing your message, {}".format(inputted_note)

            print("attempt to push!")
            print(message_string)
            
            data ={"content": message_string, "loc": {"x":0 , "y":0, "z": 0}, "type": "string"}
            url = "https://thoughtspace.firebaseio.com/.json"
            
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            
            print(r)

        else :
            speech_output = "I didn't quite hear that." 
            reprompt_text = "Sorry, what was that?"
            should_end_session = False
    else:
        speech_output = "I didn't quite hear that." 
        reprompt_text = "Sorry, what was that?"
        should_end_session = False
    
    #session_attributes = {}
    #reprompt_text = None

    #if "favoriteColor" in session.get('attributes', {}):
    #    favorite_color = session['attributes']['favoriteColor']
    #    speech_output = "Your favorite color is " + favorite_color + \
    #                    ". Goodbye."
    #    should_end_session = True
    #else:
    #    speech_output = "I'm not sure what your favorite color is. " \
    #                    "You can say, my favorite color is red."
    

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

"""        
def confirm_intent(intent, session):
    
    session_attributes = {}
    reprompt_text = ""
    should_end_session = False

    if 'Confirm' in intent['slots']:
        input_choice = intent['slots']['Confirm']['value']
    
        if (input_choice == "no"):
            speech_output = "Ok, what do you want your note to say?"
            reprompt_text = "Ok, what do you want your note to say?"
            should_end_session = False



        else:
            speech_output = "Does this look ok?"
            
            #ADD SERVER PUSHING CODE HERE FAM
            #NEVER MIND THIS GOES ELSEWHERE
            #END PUSHING CODE
            
            should_end_session = True
    else:
        speech_output = "I didn't quite hear that." 
        reprompt_text = "Sorry, what was that?"
        should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))        

    """

def wolfram_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    speech_output = ""
    reprompt_text = ""
    should_end_session = True

    
    if 'PullType' in intent['slots']:
        
        if 'value' in intent['slots']['PullType']:
            
            input_choice = intent['slots']['PullType']['value']
            #resultToChoose={"Picture": 1, "Function":2}

            if (input_choice == "picture"):
                if 'PullTarget' in intent['slots']:
                    if 'value' in intent['slots']['PullTarget']:

                        input_target = intent['slots']['PullTarget']['value']
                        client = wolframalpha.Client("26TT73-89H59Y46TE")

                        speech_output = "Found an image for {}, pushing now. ".format(input_target)
                        reprompt_text = "Found an image for {}, pushing now. ".format(input_target)

                        res = client.query(input_target+' '+input_choice)

                        i=0
                        for pod in res.pods:
                            print (pod.text)
                            i += 1
                            if(i== 2 and pod.text!= "NULL"):
                                #push_img = re.sub("gif", "jpg", pod.img)
                                #convert_image(pod.img)
                                print("about to convert and push")
                                firebase_push(convert_image(pod.img), "image")



                    else:
                        speech_output = "We could not find that pull target" 
                        reprompt_text = "We could not find that pull target" 

                else:
                    speech_output = "We could not find that pull target" 
                    reprompt_text = "We could not find that pull target" 

            elif (input_choice == "function"):
                if 'PullTarget' in intent['slots']:
                    if 'value' in intent['slots']['PullTarget']:

                        input_target = intent['slots']['PullTarget']['value']
                        client = wolframalpha.Client("26TT73-89H59Y46TE")

                        speech_output = "Found a graph for {}, pushing now. ".format(input_target)
                        reprompt_text = "Found a graph for {}, pushing now. ".format(input_target)

                        res = client.query(input_target+' '+input_choice)

                        print(res)

                        i=0
                        for pod in res.pods:
                            print (pod.text)
                            if(i>=1 and pod.text!= "NULL"):
                                #push_img = re.sub("gif", "jpg", pod.img)
                                #convert_image(pod.img)
                                print("about to convert and push")
                                firebase_push(convert_image(pod.img), "image")

                            else:
                                i=i+1

                    else:
                        speech_output = "We could not find that pull target" 
                        reprompt_text = "We could not find that pull target" 

                else:
                    speech_output = "We could not find that pull target" 
                    reprompt_text = "We could not find that pull target" 


            # elif (input_choice == "function"):
            #     if 'PullTarget' in intent['slots']:
            #         if 'value' in intent['slots']['PullTarget']:

            #             input_target = intent['slots']['PullTarget']['value']
            #             client = wolframalpha.Client("26TT73-89H59Y46TE")

            #             speech_output = "Found an graph for {}, pushing now. ".format(input_target)
            #             reprompt_text = "Found an graph for {}, pushing now. ".format(input_target)

            #             res = client.query(input_target+' '+input_choice)

            #             i=0
            #             for pod in res.pods:
            #                 print (pod.text)
            #                 if(i>=1 and pod.text!= "NULL"):
            #                     #push_img = re.sub("gif", "jpg", pod.img)
            #                     #convert_image(pod.img)
            #                     print("about to convert and push")
            #                     firebase_push(convert_image(pod.img), "image")
            #                     break;
            #                 else:
            #                     i=i+1

            #         else:
            #             speech_output = "We could not find that pull target" 
            #             reprompt_text = "We could not find that pull target" 

                # else:
                #     speech_output = "We could not find that pull target" 
                #     reprompt_text = "We could not find that pull target"

            else:
                speech_output = "That is currently not a supported pull type" 
                reprompt_text = "That is currently not a supported pull type" 

        else :
            speech_output = "I didn't quite hear that. " 
            reprompt_text = "Sorry, what was that? "
        
    else:
        speech_output = "I didn't quite hear that. " 
        reprompt_text = "Sorry, what was that? "
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))    

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'P  lainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def firebase_push(pushed_content, content_type):
    print("starting push")
    data ={"content": pushed_content, "loc": {"x":0 , "y":0, "z": 0}, "type": content_type}
    url = "https://thoughtspace.firebaseio.com/.json"
            
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)

def convert_image(pic_url):

    print("convertImage")
    api = cloudconvert.Api('f8dd1C2EAcY2y1TfRcbig-HZo-kGNKHUjR_9d3IhXYi7EnPyP1WxTYChAC7He7mMzTZEJG-ctFboNNlQuHxpyg')
    #Other API key :D
    #7pjLey9FiQhFMSvCIMHNuuALHXKIiYlSNrKY3-TcOWlHDGXBQusDvdv9zP3lKOuNv01GSN78GI_DK25XjdBW8w
    #WYSr7kqythqGEd937K0i1JLWcM-3yJKBn2VUEAPovhGV7SfK4g3MK_rXO2ru3ILqf09v23j9KTkPri32Ar-jdA

    ############################Depleted Keys
    #I5FzHhAXRON-HOBeINgZaWIQBE3D2DnG_jRdZuKP_J2InvfLyu4SY_00m9qtc_VPj-IjWACvdZ3phRP6hmXljA
    #f8dd1C2EAcY2y1TfRcbig-HZo-kGNKHUjR_9d3IhXYi7EnPyP1WxTYChAC7He7mMzTZEJG-ctFboNNlQuHxpyg 

    process = api.convert({ "input": "download", "save": "true", "filename": "in.gif", "inputformat": "gif", "outputformat": "png", "file": pic_url})
    # process.wait()

    while( process['step'] == "convert"):
        print(process['percent'])

    returned = "http:" + process['output']['url']
    return returned
