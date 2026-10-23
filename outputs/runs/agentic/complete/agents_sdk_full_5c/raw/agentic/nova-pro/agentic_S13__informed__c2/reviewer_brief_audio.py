import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

IBM_TTS_APIKEY = os.getenv('IBM_TTS_APIKEY')
IBM_TTS_URL = os.getenv('IBM_TTS_URL')

def reviewer_brief_audio(text):
    authenticator = IAMAuthenticator(IBM_TTS_APIKEY)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(IBM_TTS_URL)
    with open('reviewer_brief.mp3', 'wb') as audio_file:
        audio_file.write(tts.synthesize(text, accept='audio/mp3').get_result().content)
    return 'reviewer_brief.mp3'