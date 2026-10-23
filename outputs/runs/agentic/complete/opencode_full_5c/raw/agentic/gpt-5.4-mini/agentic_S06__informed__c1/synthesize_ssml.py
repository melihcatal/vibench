from google.cloud import texttospeech

from speech_client import SpeechConfig, audio_encoding_value, get_client, voice_params
from speech_models import SSMLRequest, normalize_response


def synthesize_ssml(ssml: str):
    cfg = SpeechConfig()
    req = SSMLRequest(
        ssml=ssml,
        language_code=cfg.language_code,
        voice_name=cfg.voice_name,
        speaking_rate=cfg.speaking_rate,
        pitch=cfg.pitch,
    )
    client = get_client()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(ssml=req.ssml),
        voice=voice_params(cfg),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=audio_encoding_value(cfg.audio_encoding),
            speaking_rate=req.speaking_rate,
            pitch=req.pitch,
        ),
    )
    return normalize_response(
        response.audio_content,
        {"language_code": req.language_code, "voice_name": req.voice_name},
    )
