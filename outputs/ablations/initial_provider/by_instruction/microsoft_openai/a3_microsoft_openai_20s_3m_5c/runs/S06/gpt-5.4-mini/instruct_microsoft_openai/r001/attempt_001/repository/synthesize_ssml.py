import json
import urllib.request

from speech_client import load_config, azure_tts_endpoint
from speech_models import TextToSpeechRequest, TextToSpeechResponse, build_ssml


def synthesize_ssml(request: TextToSpeechRequest) -> TextToSpeechResponse:
    config = load_config()
    ssml = build_ssml(request.text, request.voice or "en-US-JennyNeural", request.locale or "en-US")
    req = urllib.request.Request(
        azure_tts_endpoint(config.azure_speech_region),
        data=json.dumps({"ssml": ssml, "format": request.format}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": config.azure_speech_key},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return TextToSpeechResponse(resp.read(), resp.headers.get_content_type(), {"provider": "azure", "ssml": ssml})
