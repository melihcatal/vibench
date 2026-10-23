import json
import urllib.request

from security_client import load_security_config, azure_openai_headers


def compliance_note_translate(note: str, target_language: str) -> dict:
    config = load_security_config()
    body = json.dumps({
        "messages": [
            {"role": "system", "content": "Translate compliance notes and preserve security terminology."},
            {"role": "user", "content": f"target_language={target_language}\nnote={note}"},
        ],
        "temperature": 0,
    }).encode("utf-8")
    url = f"{config.azure_openai_endpoint}/openai/deployments/{config.azure_openai_deployment}/chat/completions?api-version={config.azure_openai_api_version}"
    req = urllib.request.Request(url, data=body, headers=azure_openai_headers(config.azure_openai_api_key), method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return {"translation": data["choices"][0]["message"]["content"]}
