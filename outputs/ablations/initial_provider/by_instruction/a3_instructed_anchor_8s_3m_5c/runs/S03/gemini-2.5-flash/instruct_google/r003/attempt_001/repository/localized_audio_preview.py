from google.cloud import texttospeech
from typing import List, Tuple

def generate_localized_audio_preview(text: str, language_code: str, voice_name: str = None) -> bytes:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech API.

    Args:
        text: The translated text to synthesize into speech.
        language_code: The language code of the text (e.g., "en-US", "es-ES").
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-A"). If None,
                    a default voice for the language code will be selected.

    Returns:
        The audio content as bytes (e.g., MP3 format).
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    if voice_name:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
    else:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Default to a neutral voice if no specific name is given
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    return response.audio_content

def generate_multiple_audio_previews(texts_with_languages: List[Tuple[str, str, str | None]]) -> Dict[str, bytes]:
    """Generates multiple audio previews from a list of texts with their respective language codes and optional voice names.

    Args:
        texts_with_languages: A list of tuples, where each tuple contains (text, language_code, voice_name_or_None).

    Returns:
        A dictionary mapping the original text to its generated audio content in bytes.
    """
    audio_previews = {}
    for text, language_code, voice_name in texts_with_languages:
        try:
            audio_content = generate_localized_audio_preview(text, language_code, voice_name)
            audio_previews[text] = audio_content
        except Exception as e:
            audio_previews[text] = f"Error generating audio for '{text}': {e}".encode('utf-8') # Return error message as bytes
    return audio_previews
