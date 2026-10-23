import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def generate_audio_preview(text):
    authenticator = IAMAuthenticator(os.getenv('IBM_TTS_APIKEY'))
    tts = TextToSpeechV1(authenticator=authenticator)
    with open('audio.mp3', 'wb') as audio_file:
        res = tts.synthesize(text, voice='en-US_AllisonV3Voice', accept='audio/mp3').get_result()
        audio_file.write(res.content)