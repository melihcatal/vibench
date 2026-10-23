import os
import requests
from safety_models import RedactionResult


def redact_unsafe(text: str) -> RedactionResult:
    """
    Identifies and redacts unsafe spans from text using the Tisane API.
    """
    api_key = os.environ.get("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable not set.")

    url = "https://api.tisane.ai/parse"

    payload = {
        "content": text,
        "language": "en",
        "settings": {
            "content_analysis": {
                "abuse": True,
                "pii": True,
            },
            "snippets": True,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return RedactionResult(
            original_text=text, redacted_text=text, flagged_spans=[{"error": str(e)}]
        )

    flagged_spans = data.get("abuse", [])
    redacted_text = list(text)

    for span in flagged_spans:
        offset = span.get("offset", 0)
        length = span.get("length", 0)
        for i in range(offset, offset + length):
            if i < len(redacted_text):
                redacted_text[i] = "*"

    return RedactionResult(
        original_text=text,
        redacted_text="".join(redacted_text),
        flagged_spans=flagged_spans,
    )
