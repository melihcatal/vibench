# platform_brief_audio.py
# [LATER-STEP] Generate spoken briefings from platform outputs using Watson Text to Speech

# Provider: IBM Watson Text to Speech
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

AUTHENTICATOR = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
client = TextToSpeechV1(authenticator=AUTHENTICATOR)
client.set_service_url(
    os.getenv("IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com")
)


def synthesize_speech(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """
    Synthesize speech audio from text using watson TTS.
    Returns raw audio bytes (default format: audio/ogg;codecs=opus).
    """
    return (
        client.synthesize_using_voice(
            text=text, accept="audio/ogg;codecs=opus", voice=voice
        )
        .get_result()
        .get_content()
    )  # returns bytes


if __name__ == "__main__":
    briefing = "Welcome to the platform briefing. Today's highlights include ..."
    audio_bytes = synthesize_speech(briefing)
    # Write to a file for demonstration
    with open("briefing.opus", "wb") as f:
        f.write(audio_bytes)
    print("Speech file 'briefing.opus' created.")
