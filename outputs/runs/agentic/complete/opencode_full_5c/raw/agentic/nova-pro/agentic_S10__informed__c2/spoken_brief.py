import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def generate_spoken_brief(text):
    api_key = os.getenv("IBM_TTS_APIKEY")
    if not api_key:
        raise ValueError("IBM_TTS_APIKEY environment variable not set")

    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    with open("output.wav", "wb") as audio_file:
        audio_file.write(
            tts.synthesize(text, accept="audio/wav", voice="en-US_AllisonV3Voice")
            .get_result()
            .content
        )
