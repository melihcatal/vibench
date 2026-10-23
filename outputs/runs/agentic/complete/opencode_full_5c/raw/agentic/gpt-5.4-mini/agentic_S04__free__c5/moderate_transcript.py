import json
import urllib.request

from speech_client import auth_headers, openai_base_url, load_speech_config


def moderate_transcript(text: str) -> dict:
    cfg = load_speech_config()
    req = urllib.request.Request(
        f"{openai_base_url()}/moderations",
        data=json.dumps({"model": "omni-moderation-latest", "input": text}).encode(
            "utf-8"
        ),
        headers={**auth_headers(), "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    data["policy_model"] = cfg.text_model
    return data
