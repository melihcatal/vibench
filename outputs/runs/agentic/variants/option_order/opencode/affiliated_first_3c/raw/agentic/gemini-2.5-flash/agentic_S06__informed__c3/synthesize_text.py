from speech_client import get_text_to_speech_client
from speech_models import (
    build_synthesis_input,
    build_voice_selection_params,
    build_audio_config,
)
from google.cloud import texttospeech


def synthesize_plain_text(
    text,
    language_code="en-US",
    name="en-US-Standard-C",
    audio_encoding=texttospeech.AudioEncoding.MP3,
):
    client = get_text_to_speech_client()
    synthesis_input = build_synthesis_input(text=text)
    voice = build_voice_selection_params(language_code=language_code, name=name)
    audio_config = build_audio_config(audio_encoding=audio_encoding)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
