import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def generate_spoken_brief(text: str) -> str:
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(os.getenv("IBM_TTS_URL"))
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(tts.synthesize(text, accept="audio/mp3").get_result().content)
    return "output.mp3"
