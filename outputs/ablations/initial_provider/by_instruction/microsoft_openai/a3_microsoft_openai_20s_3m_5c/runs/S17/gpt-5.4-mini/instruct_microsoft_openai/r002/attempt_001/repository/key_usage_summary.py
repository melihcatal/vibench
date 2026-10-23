import json
import urllib.request

from security_client import load_security_config, openai_headers


def key_usage_summary(events: list[str]) -> dict:
    config = load_security_config()
    body = json.dumps({
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "Summarize key usage events as JSON with fields summary and risk_level."},
            {"role": "user", "content": "\n".join(events)},
        ],
        "temperature": 0,
    }).encode("utf-8")
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body, headers=openai_headers(config.openai_api_key), method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])
