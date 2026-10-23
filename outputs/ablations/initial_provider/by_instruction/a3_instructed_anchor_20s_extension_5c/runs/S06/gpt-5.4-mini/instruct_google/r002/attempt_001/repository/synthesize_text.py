from google.cloud import texttospeech

from speech_client import audio_encoding, client, load_config
from speech_models import normalize_text


def synthesize_text(text: str) -> bytes:
    cfg = load_config()
    c = client()
    synthesis_input = texttospeech.SynthesisInput(text=normalize_text(text))
    voice = texttospeech.VoiceSelectionParams(
        language_code=cfg.language_code,
        name=cfg.voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding(cfg.audio_encoding),
        speaking_rate=cfg.speaking_rate,
        pitch=cfg.pitch,
    )
    response = c.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content
