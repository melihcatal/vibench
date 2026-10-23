import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

api_key = os.getenv("IBM_TTS_APIKEY")
url = os.getenv("IBM_TTS_URL")

authenticator = IAMAuthenticator(api_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url)


def generate_spoken_brief(text):
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept="audio/mp3").get_result().content
        )
        print("Spoken brief generated as output.mp3")
