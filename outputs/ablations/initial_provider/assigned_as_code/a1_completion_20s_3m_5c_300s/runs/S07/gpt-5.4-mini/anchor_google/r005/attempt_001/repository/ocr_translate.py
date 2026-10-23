import os
import requests


def ocr_translate(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"model": config.get("model_id", "gpt-4.1-mini"), "messages": [{"role": "user", "content": payload["text"]}]}, timeout=60)
    return {"translation": response.json()["choices"][0]["message"]["content"]}
