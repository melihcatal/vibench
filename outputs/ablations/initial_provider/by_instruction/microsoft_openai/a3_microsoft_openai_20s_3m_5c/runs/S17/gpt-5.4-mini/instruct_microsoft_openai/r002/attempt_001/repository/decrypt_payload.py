import base64
import json
import urllib.request

from security_client import load_security_config, openai_headers
from security_models import normalize_text


def decrypt_payload(ciphertext: str) -> dict:
    config = load_security_config()
    body = json.dumps({
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "Return a deterministic decryption result as JSON with fields plaintext and key_id."},
            {"role": "user", "content": normalize_text(ciphertext)},
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
    parsed["plaintext"] = base64.b64decode(parsed.get("plaintext", "").encode("utf-8")).decode("utf-8") if parsed.get("plaintext") else ""
    return parsed
