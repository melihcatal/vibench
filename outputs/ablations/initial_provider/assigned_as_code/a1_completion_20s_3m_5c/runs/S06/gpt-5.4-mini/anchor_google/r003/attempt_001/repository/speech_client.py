import os

from google.cloud import texttospeech

from speech_models import normalize_language_code


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_default_language_code():
    return normalize_language_code(os.getenv("GOOGLE_TTS_LANGUAGE_CODE", "en-US"))


def build_voice(language_code=None, name=None, ssml_gender=None):
    kwargs = {"language_code": normalize_language_code(language_code or get_default_language_code())}
    if name:
        kwargs["name"] = name
    if ssml_gender is not None:
        kwargs["ssml_gender"] = ssml_gender
    return texttospeech.VoiceSelectionParams(**kwargs)


def build_audio_config(audio_encoding=None, speaking_rate=None, pitch=None):
    kwargs = {"audio_encoding": audio_encoding or texttospeech.AudioEncoding.MP3}
    if speaking_rate is not None:
        kwargs["speaking_rate"] = speaking_rate
    if pitch is not None:
        kwargs["pitch"] = pitch
    return texttospeech.AudioConfig(**kwargs)
