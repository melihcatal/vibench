import os
from google.cloud import speech_v1 as speech
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_google_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return speech.SpeechClient()

def get_ibm_speech_client():
    apikey = os.environ.get('IBM_STT_APIKEY')
    url = os.environ.get('IBM_STT_URL')
    authenticator = IAMAuthenticator(apikey)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(url)
    return speech_to_text