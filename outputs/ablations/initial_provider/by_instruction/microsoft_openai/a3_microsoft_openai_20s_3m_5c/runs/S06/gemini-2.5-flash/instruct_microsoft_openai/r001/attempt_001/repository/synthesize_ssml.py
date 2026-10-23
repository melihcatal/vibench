from google.cloud import texttospeech
import os

def synthesize_ssml(ssml_text: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """
    Synthesizes SSML text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the language and SSML voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
