from typing import Dict

import requests

OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY = __import__("os").getenv("OPENAI_API_KEY", "")


def check_document_safety(text: str, api_key: str = "") -> Dict[str, object]:
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OpenAI API key is required")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_MODERATION_URL, headers=headers, json={"model": OPENAI_MODERATION_MODEL, "input": text}, timeout=60)
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return {"flagged": result["flagged"], "categories": result.get("categories", {}), "raw": data}
