import os
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
import json


def generate_spoken_brief(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Generate an audio brief from model output using IBM Watson Text-to-Speech."""
    api_key = os.getenv("IBM_TTS_APIKEY", "<INSERT_TTS_APIKEY>")
    url = os.getenv(
        "IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com"
    )
    tts = TextToSpeechV1(authenticator=TextToSpeechV1.IamAuthenticator(api_key))
    tts.set_service_url(url)

    # Use websocket streaming for immediate audio
    class Callback(SynthesizeCallback):
        def __init__(self):
            super().__init__()
            self.audio = b""

        def on_data(self, data):
            self.audio += data

        def get_audio(self):
            return self.audio

    callback = Callback()
    tts.synthesize_using_websocket(
        text,
        callback=callback,
        accept="audio/lpcm",
        voice=voice,
    )
    return callback.get_audio()
