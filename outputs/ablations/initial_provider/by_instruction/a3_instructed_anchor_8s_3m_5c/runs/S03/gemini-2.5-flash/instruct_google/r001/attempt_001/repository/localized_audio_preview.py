import os
from google.cloud import texttospeech

def generate_audio_preview(
    translated_text: str, language_code: str, voice_name: str = None
) -> bytes:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech API.

    Args:
        translated_text: The translated text to convert to speech.
        language_code: The BCP-47 language code for the voice (e.g., 'en-US', 'es-ES').
                       This should ideally match the target language of the translation.
        voice_name: The name of the voice to use (e.g., 'en-US-Wavenet-D'). If not provided,
                    a suitable voice for the language code will be selected.

    Returns:
        The audio content as bytes (e.g., MP3 format).
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=translated_text)

    # Select the language and SSML voice gender
    # You can explore available voices using the client.list_voices() method.
    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,  # Use specific voice if provided
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Default to neutral
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice_selection_params,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary. You can save it to a file or stream it.
    return response.audio_content
