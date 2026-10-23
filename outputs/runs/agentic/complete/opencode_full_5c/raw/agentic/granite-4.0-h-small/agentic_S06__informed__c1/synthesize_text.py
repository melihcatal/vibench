# synthesize_text.py
import os
from google.cloud import texttospeech


def synthesize(text, voice="en-US-Wavenet-D", language_code="en-US"):
    client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(text=text)
    voice_config = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_ssml, voice=voice_config, audio_config=audio_config
    )
    return response.audio_content
