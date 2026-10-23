import json
import urllib.request

from vision_client import load_vision_config
from vision_models import normalize_translation_response


def alt_text_translate(payload, config=None):
    config = load_vision_config(config)
    body = {
        "model": config["openai_model"],
        "messages": [
            {"role": "user", "content": f"Translate the following image description to {config['target_language']}: {payload.get('description', '')}"}
        ],
        "max_tokens": 128,
    }
    req = urllib.request.Request(
        f"{config['openai_base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return normalize_translation_response({"translation": data["choices"][0]["message"]["content"].strip(), "language": config["target_language"]})
