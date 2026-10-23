import os
import requests


def ocr_safety(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
    response = requests.post("https://api.openai.com/v1/moderations", headers={"Authorization": f"Bearer {api_key}"}, json={"model": config.get("model_id", "omni-moderation-latest"), "input": payload["text"]}, timeout=60)
    return {"result": response.json()}
