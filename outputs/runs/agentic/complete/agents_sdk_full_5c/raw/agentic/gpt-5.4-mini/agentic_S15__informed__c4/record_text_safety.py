from typing import Any, Dict

import requests

TISANE_ENDPOINT = "https://api.tisane.ai/parse"


def check_record_text_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = requests.utils.os.getenv("TISANE_API_KEY") if hasattr(requests.utils, "os") else None
    headers = {"x-api-key": api_key} if api_key else {}
    payload = {"content": text, "language": language}
    response = requests.post(TISANE_ENDPOINT, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return {"provider": "Tisane", "result": response.json()}
