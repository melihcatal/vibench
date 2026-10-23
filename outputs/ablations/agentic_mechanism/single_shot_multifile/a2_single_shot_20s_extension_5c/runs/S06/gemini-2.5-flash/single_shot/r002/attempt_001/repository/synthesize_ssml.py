import os
from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import AudioOutputConfig

def synthesize_ssml_text(
    ssml_text: str,
    voice_name: str = "en-US-Wavenet-D",
    language_code: str = "en-US",
    gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL,
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
    sample_rate_hertz: int = 24000
) -> bytes:
    """
    Synthesizes SSML text into audio bytes using Google Cloud Text-to-Speech,
    allowing for voice and prosody controls embedded in the SSML.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        sample_rate_hertz=sample_rate_hertz
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
