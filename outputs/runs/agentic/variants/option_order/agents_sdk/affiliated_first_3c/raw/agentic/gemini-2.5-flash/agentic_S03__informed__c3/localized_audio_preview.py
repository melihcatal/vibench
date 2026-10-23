from google.cloud import texttospeech
import os

def generate_spoken_preview(text: str, language_code: str, voice_name: str = None) -> bytes:
    """
    Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.
    Returns audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    if voice_name:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
    else:
        # Default to a suitable voice if not specified
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
