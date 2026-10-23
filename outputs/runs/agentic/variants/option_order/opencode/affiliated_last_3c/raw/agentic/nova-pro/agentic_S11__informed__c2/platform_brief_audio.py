import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def generate_audio(text):
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    tts = TextToSpeechV1(authenticator=authenticator)
    with open("output.wav", "wb") as audio_file:
        res = tts.synthesize(
            text, accept="audio/wav", voice="en-US_AllisonV3Voice"
        ).get_result()
        audio_file.write(res.content)
