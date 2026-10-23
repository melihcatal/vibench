from google.cloud import texttospeech
from speech_models import make_input, make_voice, make_audio_config
from typing import Optional


def synthesize_ssml(
    ssml: str,
    voice_name: str = "en-US-Standard-A",
    encoding: str = "MP3",
    **audio_kwargs,
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = make_input(ssml=ssml)
    voice = make_voice(voice_name)
    audio_config = make_audio_config(encoding=encoding, **audio_kwargs)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
