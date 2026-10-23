import base64
import json
import urllib.request

from security_client import load_security_config, openai_headers
from security_models import PayloadRequest, normalize_text


def encrypt_payload(plaintext: str) -> dict:
    config = load_security_config()
    request = PayloadRequest(plaintext=normalize_text(plaintext))
    body = json.dumps({
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "Return a deterministic encryption envelope as JSON with fields ciphertext and key_id."},
            {"role": "user", "content": request.plaintext},
        ],
        "temperature": 0,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers=openai_headers(config.openai_api_key),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    parsed["ciphertext"] = base64.b64encode(parsed.get("ciphertext", "").encode("utf-8")).decode("utf-8")
    return parsed
