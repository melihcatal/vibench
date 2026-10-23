import json
import urllib.request

from speech_client import google_speech_headers, load_speech_config, normalize_uri
from speech_models import TranscriptionRequest, build_google_speech_payload


def submit_transcription(audio_uri: str, language_code: str = "en-US"):
    config = load_speech_config()
    request = TranscriptionRequest(source_uri=normalize_uri(audio_uri), language_code=language_code, model=config.google_model)
    payload = build_google_speech_payload(request)
    req = urllib.request.Request(
        "https://speech.googleapis.com/v1/speech:longrunningrecognize",
        data=json.dumps(payload).encode("utf-8"),
        headers=google_speech_headers(config.google_api_key),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))
