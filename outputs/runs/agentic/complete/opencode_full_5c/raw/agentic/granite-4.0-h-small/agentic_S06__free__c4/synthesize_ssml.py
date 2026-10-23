# [SAME-SCENARIO] synthesize_ssml.py
# Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech

from google.cloud import texttospeech


def synthesize(ssml: str, voice: str = "en-US-Wavenet-D") -> bytes:
    client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=ssml)
    voice_config = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    )
    response = client.synthesize_speech(
        input=input_ssml,
        voice=voice_config,
        audio_config=audio_config,
    )
    return response.audio_content  # bytes object
