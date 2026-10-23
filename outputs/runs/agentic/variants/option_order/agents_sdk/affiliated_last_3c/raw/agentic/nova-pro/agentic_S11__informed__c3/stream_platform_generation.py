import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = os.environ['IBM_TTS_APIKEY']
url = os.environ['IBM_TTS_URL']

authenticator = IAMAuthenticator(apikey)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url)

def stream_generation(text):
    response = text_to_speech.synthesize(text, voice='en-US_AllisonV3Voice', accept='audio/mp3')
    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(response.content)
        audio_file.close()