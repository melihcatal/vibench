import json
import urllib.request

from speech_client import load_speech_config


def transcript_embedding(text: str):
    config = load_speech_config()
    payload = {"model": "text-embedding-3-small", "input": text}
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config.openai_api_key or ''}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))
