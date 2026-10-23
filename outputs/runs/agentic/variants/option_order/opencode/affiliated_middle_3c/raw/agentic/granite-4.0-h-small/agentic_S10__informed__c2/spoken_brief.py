# Generate spoken brief using IBM Watson Text-to-Speech SDK

import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from model_client import parse_chat_response

# -------------------------------------------------
# IBM Watson Text-to-Speech configuration
# -------------------------------------------------
WATSON_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
WATSON_TTS_URL = os.getenv(
    "IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com"
)

authenticator = IAMAuthenticator(WATSON_TTS_APIKEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(WATSON_TTS_URL)


def generate_spoken_brief(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Generate an audio file (bytes) from text using IBM Watson TTS."""
    response = tts.synthesize(text, accept="audio/wav", voice=voice).get_result()
    # Return raw audio bytes
    return response.content


# Example (uncomment to test)
# audio_bytes = generate_spoken_brief("Welcome to the briefing.")
# with open('brief.wav', 'wb') as f:
#     f.write(audio_bytes)
