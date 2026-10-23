import os
from typing import List, Optional

from google.cloud import texttospeech_v1 as texttospeech


def localized_audio_preview(
    texts: List[str],
    language_code: str,
    voice_name: Optional[str] = None,
    output_format: str = "MP3",
) -> List[bytes]:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech.

    Args:
        texts: List of translated texts to convert to speech.
        language_code: The language code for the voice (e.g., 'es-ES').
        voice_name: Optional specific voice name (e.g., 'es-ES-Standard-A').
        output_format: The audio output format (default: 'MP3').

    Returns:
        List of audio bytes for each input text.

    Raises:
        ValueError: If the input list is empty or Google Cloud TTS API call fails.
    """
    if not texts:
        raise ValueError("Texts cannot be empty")

    client = texttospeech.TextToSpeechClient()

    audio_contents = []
    for text in texts:
        if not text.strip():
            continue

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name or f"{language_code}-Standard-A",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, output_format.upper())
        )

        try:
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            audio_contents.append(response.audio_content)
        except Exception as e:
            raise ValueError(f"Failed to generate audio preview: {e}")

    return audio_contents
