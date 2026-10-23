from google.cloud import texttospeech

from speech_client import SpeechConfig, audio_encoding_value, get_client, voice_params
from speech_models import TextRequest, normalize_response, normalize_text


def synthesize_text(text: str):
    cfg = SpeechConfig()
    req = TextRequest(
        text=normalize_text(text),
        language_code=cfg.language_code,
        voice_name=cfg.voice_name,
    )
    client = get_client()
    synthesis_input = texttospeech.SynthesisInput(text=req.text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params(cfg),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=audio_encoding_value(cfg.audio_encoding),
            speaking_rate=cfg.speaking_rate,
            pitch=cfg.pitch,
        ),
    )
    return normalize_response(
        response.audio_content,
        {"language_code": req.language_code, "voice_name": req.voice_name},
    )
