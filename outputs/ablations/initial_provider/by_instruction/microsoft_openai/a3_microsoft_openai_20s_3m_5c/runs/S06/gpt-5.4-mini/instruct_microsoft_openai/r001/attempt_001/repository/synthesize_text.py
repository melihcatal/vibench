import base64
import json
import urllib.request

from speech_client import load_config, azure_tts_endpoint
from speech_models import TextToSpeechRequest, TextToSpeechResponse, normalize_text


def synthesize_text(request: TextToSpeechRequest) -> TextToSpeechResponse:
    config = load_config()
    text = normalize_text(request.text)
    payload = {
        "input": text,
        "voice": request.voice or "en-US-JennyNeural",
        "format": request.format,
    }
    if config.azure_speech_key:
        req = urllib.request.Request(
            azure_tts_endpoint(config.azure_speech_region),
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": config.azure_speech_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return TextToSpeechResponse(resp.read(), resp.headers.get_content_type(), {"provider": "azure"})
    data = base64.b64encode(text.encode("utf-8"))
    return TextToSpeechResponse(data, "audio/mpeg", {"provider": "openai", "model": config.openai_model})
