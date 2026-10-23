import os
from speech_client import TextToSpeechClient

def synthesize_ssml(ssml):
    # Initialize TTS client using environment variables for credentials
    client = TextToSpeechClient()
    # Request SSML synthesis with optional voice and prosody overrides
    response = client.synthesize_speech(
        input_text=ssml,
        voice_name=None,
        audio_format='LINEAR16'
    )
    return response.audio_content
