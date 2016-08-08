"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import pyowm
owm = pyowm.OWM('89a38199527cc52e90ba03a0db40191c')


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
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
    if intent_name == "MyCityIntent":
        return set_city_in_session(intent, session)
    if intent_name == "MyStateIntent":
        return set_state_in_session(intent, session)
    elif intent_name == "WhatsWeatherIntent":
        return get_weather_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
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
    speech_output = "Welcome to the mini lab 8. " \
                    "Ask me what the weather is by saying, " \
                    "what is the weather?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask me what the weather is by saying, " \
                    "what is the weather?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the mini lab 8 " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_city_in_session(intent, session):
    """
    Sets the location of a city
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False


    if 'City' in intent['slots']:
        current_city = intent['slots']['City']['value']
        session_attributes['city'] = current_city
        speech_output = "I now know your city is " + \
                        current_city + \
                        ". You can now set your state by saying, " \
                        "my state is Washington?"
        reprompt_text = "You can now set your state by saying, " \
                        "my state is Washington?"
    else: 
        speech_output = "I am not sure which city you are in. " \
                        "Please try again."
        reprompt_text = "I'm not sure which city you are in. " \
                        "You can tell me which city you are in by saying, " \
                        "my city Seattle"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_state_in_session(intent, session):
    """
    Sets the location of a state
    """
    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False


    if 'State' in intent['slots']:
        current_state = intent['slots']['State']['value']
        session_attributes['state'] = current_state
        speech_output = "I now know your state is " + \
                        current_state + \
                        ". You can ask me the weather by saying, " \
                        "what's the weather?"
        reprompt_text = "You can ask me the weather by saying " \
                        "what's the weather?"
    else: 
        speech_output = "I am not sure which state you are in. " \
                        "Please try again."
        reprompt_text = "I'm not sure which state you are in. " \
                        "You can tell me which state you are in by saying, " \
                        "my state is Washington?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_weather_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    session_attributes = session.get('attributes', {})

    if session_attributes and "city" in session_attributes and "state" in session_attributes:
        current_city = session['attributes']['city']
        current_state = session['attributes']['state']
        obs = owm.weather_at_place(current_city + ', ' + current_state + ',' + ' US')
        w = obs.get_weather().get_detailed_status()

        speech_output = "The weather in " + current_city + ", " + current_state +  \
                        " is " + w + ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not so sure what the weather is. " \
                        "You can say, what's the weather"
        should_end_session = False
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

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
                'type': 'PlainText',
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
