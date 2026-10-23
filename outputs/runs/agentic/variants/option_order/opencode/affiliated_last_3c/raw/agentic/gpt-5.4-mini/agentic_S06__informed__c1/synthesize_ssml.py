from speech_client import client, load_config, synthesize_request
from speech_models import SpeechRequest, normalize_ssml, response_to_bytes


def synthesize_ssml(ssml: str, voice_id: str | None = None) -> bytes:
    cfg = load_config()
    req = SpeechRequest(
        text=normalize_ssml(ssml), voice_id=voice_id or cfg.default_voice, ssml=True
    )
    polly = client(cfg)
    response = polly.synthesize_speech(
        **synthesize_request(req.text, req.voice_id or "Joanna", True, cfg)
    )
    return response_to_bytes(response)
