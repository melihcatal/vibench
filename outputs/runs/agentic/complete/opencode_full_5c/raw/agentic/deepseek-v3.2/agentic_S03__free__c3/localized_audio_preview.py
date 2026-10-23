import os
import tempfile
from typing import Optional, Dict, Any
from google.cloud import texttospeech


def generate_spoken_preview(
    text: str, language_code: str, output_format: str = "mp3"
) -> Dict[str, Any]:
    """
    Generate spoken audio preview of translated copy using Google Cloud Text-to-Speech API.

    Args:
        text: Text to convert to speech
        language_code: Language code for speech synthesis (e.g., 'en-US', 'es-ES')
        output_format: Output audio format ('mp3', 'wav', 'ogg')

    Returns:
        Dictionary with audio information and file path
    """
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file
    if output_format == "mp3":
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
    elif output_format == "wav":
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
    elif output_format == "ogg":
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
        )
    else:
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Create a temporary file for the audio
    with tempfile.NamedTemporaryFile(
        suffix=f".{output_format}", delete=False
    ) as temp_file:
        temp_file.write(response.audio_content)
        temp_path = temp_file.name

    # Get voice details
    voice_name = voice.language_code

    return {
        "audio_file_path": temp_path,
        "text_length": len(text),
        "language_code": language_code,
        "output_format": output_format,
        "voice_used": voice_name,
        "audio_size_bytes": len(response.audio_content),
        "provider": "Google Cloud Text-to-Speech API",
    }


def get_available_voices(language_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get available voices for text-to-speech synthesis.

    Args:
        language_code: Optional language code filter

    Returns:
        List of available voices
    """
    client = texttospeech.TextToSpeechClient()

    voices_response = client.list_voices(language_code=language_code)

    voices = []
    for voice in voices_response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_code": voice.language_codes[0],
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )

    return voices
