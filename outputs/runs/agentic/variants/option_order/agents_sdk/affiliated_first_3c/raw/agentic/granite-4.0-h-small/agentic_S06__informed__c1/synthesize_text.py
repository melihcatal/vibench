import os
from speech_client import TextToSpeechClient

def synthesize_text(text):
    # Initialize TTS client using environment variables for credentials
    client = TextToSpeechClient()
    # Request plain text synthesis
    response = client.synthesize_speech(
        input_text=text,
        voice_name=None,  # uses default or selected voice (handled elsewhere)
        audio_format='LINEAR16'
    )
    # response.audio_content is a byte string of the audio stream
    return response.audio_content
