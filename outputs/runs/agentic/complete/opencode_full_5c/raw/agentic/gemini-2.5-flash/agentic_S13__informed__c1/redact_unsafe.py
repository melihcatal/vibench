import os
import requests
import json

TISANE_API_KEY = os.environ.get("TISANE_API_KEY")
TISANE_API_ENDPOINT = "https://api.tisane.ai/parse"


def redact_unsafe(text: str):
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": TISANE_API_KEY,
    }
    data = {
        "language": "en",
        "text": text,
        "settings": {"token_attributes": ["sentence_start", "is_safe"]},
    }
    response = requests.post(
        TISANE_API_ENDPOINT, headers=headers, data=json.dumps(data)
    )
    response.raise_for_status()
    result = response.json()
    redacted_text = ""
    offset = 0
    if "annotations" in result:
        for annotation in result["annotations"]:
            start = annotation["start"]
            end = annotation["end"]
            redacted_text += text[offset:start]
            redacted_text += "[REDACTED]"
            offset = end
    redacted_text += text[offset:]
    return redacted_text, result
