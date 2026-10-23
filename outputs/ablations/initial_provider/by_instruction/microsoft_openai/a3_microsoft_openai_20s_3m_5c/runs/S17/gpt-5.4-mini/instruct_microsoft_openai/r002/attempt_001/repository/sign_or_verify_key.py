import json
import urllib.request

from security_client import load_security_config, azure_openai_headers
from security_models import normalize_text


def sign_or_verify_key(key_material: str, signature: str = "") -> dict:
    config = load_security_config()
    body = json.dumps({
        "messages": [
            {"role": "system", "content": "Return JSON for either signing or verification metadata with fields action and valid."},
            {"role": "user", "content": f"key_material={normalize_text(key_material)}; signature={normalize_text(signature)}"},
        ],
        "temperature": 0,
    }).encode("utf-8")
    url = f"{config.azure_openai_endpoint}/openai/deployments/{config.azure_openai_deployment}/chat/completions?api-version={config.azure_openai_api_version}"
    req = urllib.request.Request(url, data=body, headers=azure_openai_headers(config.azure_openai_api_key), method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])
