from speech_client import get_text_to_speech_client
from speech_models import (
    build_synthesis_input,
    build_voice_selection_params,
    build_audio_config,
)
from google.cloud import texttospeech


def synthesize_plain_text(
    text: str, language_code: str = "en-US", voice_name: str = None
) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_text_to_speech_client()
    synthesis_input = build_synthesis_input(text=text)
    voice = build_voice_selection_params(language_code=language_code, name=voice_name)
    audio_config = build_audio_config()

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
