import os
from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import TextSynthesisRequest, AudioOutputConfig

def synthesize_plain_text(
    text: str,
    voice_name: str = "en-US-Wavenet-C",
    language_code: str = "en-US",
    gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume_gain_db: float = 0.0,
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
    sample_rate_hertz: int = 24000
) -> bytes:
    """
    Synthesizes plain text into audio bytes using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
        sample_rate_hertz=sample_rate_hertz
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
