from google.cloud import texttospeech

from speech_client import build_client, load_config
from speech_models import normalize_ssml


def synthesize_ssml(ssml: str, voice_name: str | None = None, speaking_rate: float | None = None, pitch: float | None = None) -> bytes:
    cfg = load_config()
    client = build_client()
    input_ssml = texttospeech.SynthesisInput(ssml=normalize_ssml(ssml))
    voice = texttospeech.VoiceSelectionParams(language_code=cfg.default_language_code, name=voice_name or cfg.default_voice_name or "")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate if speaking_rate is not None else cfg.default_speaking_rate, pitch=pitch if pitch is not None else cfg.default_pitch)
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    return response.audio_content
