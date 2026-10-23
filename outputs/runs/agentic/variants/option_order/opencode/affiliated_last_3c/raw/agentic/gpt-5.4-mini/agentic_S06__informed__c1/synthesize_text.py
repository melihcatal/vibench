from speech_client import client, load_config, synthesize_request
from speech_models import SpeechRequest, normalize_text, response_to_bytes


def synthesize_text(text: str, voice_id: str | None = None) -> bytes:
    cfg = load_config()
    req = SpeechRequest(
        text=normalize_text(text), voice_id=voice_id or cfg.default_voice
    )
    polly = client(cfg)
    response = polly.synthesize_speech(
        **synthesize_request(req.text, req.voice_id or "Joanna", False, cfg)
    )
    return response_to_bytes(response)
