import base64
import json
import urllib.request

from vision_client import load_vision_config
from vision_models import normalize_description_response


def describe_image(payload, config=None):
    config = load_vision_config(config)
    image_bytes = payload["image_bytes"]
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    body = {
        "model": config["openai_model"],
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Write a short visual description of this image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]}
        ],
        "max_tokens": 64,
    }
    req = urllib.request.Request(
        f"{config['openai_base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return normalize_description_response({"description": data["choices"][0]["message"]["content"].strip()})
