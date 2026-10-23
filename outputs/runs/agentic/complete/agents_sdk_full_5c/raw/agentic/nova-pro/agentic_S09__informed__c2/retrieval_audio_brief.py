import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_TTS_APIKEY'))
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(os.getenv('IBM_TTS_URL'))

def generate_audio_brief(text):
    with open('audio_brief.mp3', 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(text, voice='en-US_AllisonV3Voice', accept='audio/mp3').get_result().content)