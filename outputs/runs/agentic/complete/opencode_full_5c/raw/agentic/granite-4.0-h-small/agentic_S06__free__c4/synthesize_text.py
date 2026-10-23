# [SAME-SCENARIO] synthesize_text.py
# Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech

from google.cloud import texttospeech
from typing import byte array

def synthesize(text: str, voice: str = "en-US-Standard-B") -> bytearray:
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice_config = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    )
    response = client.synthesize_speech(
        input=input_text,
        voice=voice_config,
        audio_config=audio_config,
    )
    # response.audio_content is a byte string
    return bytearray(response.audio_content)
