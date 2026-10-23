import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

authenticator = IAMAuthenticator(IBM_TTS_APIKEY)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(IBM_TTS_URL)


def generate_briefing(text):
    with open("briefing.mp3", "wb") as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept="audio/mp3").get_result().content
        )
