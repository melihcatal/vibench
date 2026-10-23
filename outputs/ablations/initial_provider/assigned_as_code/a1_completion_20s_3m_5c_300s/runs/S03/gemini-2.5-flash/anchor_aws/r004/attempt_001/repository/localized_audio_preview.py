from google.cloud import texttospeech
import os

def generate_audio_preview(text: str, language_code: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    # Initialize the Google Cloud Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice (e.g., "en-US-Wavenet-D" for a US English Wavenet voice)
    # The voice_name here is a concrete identifier for a specific voice.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Save it or return it.
    return response.audio_content
