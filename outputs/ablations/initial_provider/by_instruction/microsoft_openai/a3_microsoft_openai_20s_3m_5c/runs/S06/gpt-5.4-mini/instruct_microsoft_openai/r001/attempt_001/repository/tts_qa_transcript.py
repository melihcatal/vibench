import json
import urllib.request

from speech_client import load_config, openai_base_url


def transcribe_qa_audio(audio_bytes: bytes):
    config = load_config()
    req = urllib.request.Request(
        f"{openai_base_url()}/audio/transcriptions",
        data=json.dumps({"model": "gpt-4o-mini-transcribe", "audio": audio_bytes.hex()}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config.openai_api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")
