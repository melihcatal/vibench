import os
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

load_dotenv()

TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
TTS_URL = os.getenv("IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com")

authenticator = IAMAuthenticator(TTS_APIKEY)
tts = TextToSpeechV1(authenticator=authenticator)

def retrieve_audio_brief(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Generate an audio brief from retrieved search results using Watson TTS."""
    response = tts.synthesize(text=text, accept="audio/wav", voice=voice).get_result()
    return response.content
