import requests

from speech_client import load_config, build_headers
from speech_models import SynthesisRequest, normalize_text


def synthesize_text(text: str) -> bytes:
    cfg = load_config()
    req = SynthesisRequest(text=normalize_text(text), voice_id=cfg.voice)
    response = requests.post(
        f"{cfg.base_url}/text-to-speech/{req.voice_id or 'default'}",
        headers=build_headers(cfg.api_key),
        json={"text": req.text, "model_id": req.model_id},
        timeout=60,
    )
    response.raise_for_status()
    return response.content
