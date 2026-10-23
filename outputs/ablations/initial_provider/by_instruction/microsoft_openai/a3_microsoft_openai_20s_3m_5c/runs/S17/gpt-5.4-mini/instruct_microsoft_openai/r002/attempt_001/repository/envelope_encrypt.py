import json
import urllib.request

from security_client import load_security_config, azure_openai_headers
from security_models import normalize_text


def envelope_encrypt(payload: str, key_id: str) -> dict:
    config = load_security_config()
    body = json.dumps({
        "messages": [
            {"role": "system", "content": "Produce an envelope-encryption plan as JSON with wrapped_key and data_key fields."},
            {"role": "user", "content": f"payload={normalize_text(payload)}; key_id={normalize_text(key_id)}"},
        ],
        "temperature": 0,
    }).encode("utf-8")
    url = f"{config.azure_openai_endpoint}/openai/deployments/{config.azure_openai_deployment}/chat/completions?api-version={config.azure_openai_api_version}"
    req = urllib.request.Request(url, data=body, headers=azure_openai_headers(config.azure_openai_api_key), method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])
