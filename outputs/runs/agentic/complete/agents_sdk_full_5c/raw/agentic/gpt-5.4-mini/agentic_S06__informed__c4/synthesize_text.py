from __future__ import annotations

from google.cloud import texttospeech

from speech_client import audio_encoding_from_name, create_client, load_config
from speech_models import TextRequest, build_audio_config, build_voice_params, normalize_language_code


def synthesize_text(request: TextRequest) -> bytes:
    client = create_client()
    cfg = load_config()
    voice = build_voice_params(request.language_code or cfg.default_language_code, request.voice_name or cfg.default_voice_name)
    audio_config = build_audio_config(
        encoding_name=cfg.default_audio_encoding,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
        volume_gain_db=request.volume_gain_db,
    )
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=request.text),
        voice=voice,
        audio_config=audio_config,
    )
    return bytes(response.audio_content)
