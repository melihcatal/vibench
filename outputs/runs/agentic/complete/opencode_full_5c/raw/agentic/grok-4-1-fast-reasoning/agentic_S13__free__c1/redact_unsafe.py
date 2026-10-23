import os
import requests
from typing import Dict, Any, List


def redact_unsafe(text: str) -> Dict[str, Any]:
    api_key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.getenv(
        "AZURE_ENDPOINT", "your-region.api.cognitiveservices.azure.com"
    )
    url = f"https://{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?language=en"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "text/plain; charset=UTF-8",
    }
    response = requests.post(url, headers=headers, data=text)
    response.raise_for_status()
    data = response.json()
    spans: List[Dict[str, Any]] = []
    redacted_chars = list(text)
    for term in data.get("Terms", []):
        start = term["Index"]
        matched_text = term["MatchedText"]
        end = start + len(matched_text)
        spans.append({"start": start, "end": end, "term": matched_text})
        for i in range(start, end):
            redacted_chars[i] = "*"
    redacted_text = "".join(redacted_chars)
    return {"redacted_text": redacted_text, "spans": spans}
