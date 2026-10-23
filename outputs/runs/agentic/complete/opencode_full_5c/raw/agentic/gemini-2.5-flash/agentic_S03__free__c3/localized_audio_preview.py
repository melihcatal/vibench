from google.cloud import texttospeech_v1
from typing import Tuple, Dict, Any


def generate_spoken_preview(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"
) -> Tuple[bytes, str]:
    """Generates a spoken audio preview of translated copy using Google Cloud Text-to-Speech API.

    Args:
        text: The translated text to convert to speech.
        language_code: The BCP-47 language code for the voice (e.g., "en-US", "es-ES").
        voice_name: The name of the voice to use (e.g., "en-US-Standard-A").

    Returns:
        A tuple containing:
        - The audio content as bytes (e.g., MP3 data).
        - The MIME type of the audio content (e.g., "audio/mp3").
    """
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    return response.audio_content, "audio/mp3"
