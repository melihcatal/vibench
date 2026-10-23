import requests
import os
from typing import List, Dict, Any
from safety_models import UnsafeSpan, RedactionResult
from safety_client import get_api_key


def redact_unsafe(text: str) -> Dict[str, Any]:
    api_key = get_api_key("AZURE_CONTENT_MODERATOR_KEY")
    region = os.getenv("AZURE_CONTENT_MODERATOR_REGION", "westus")
    endpoint = f"https://{region}.api.cognitiveservices.azure.com"
    url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?language=eng&amp;autocorrect=true"
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "text/plain"}
    response = requests.post(url, headers=headers, data=text)
    response.raise_for_status()
    data = response.json()
    spans: List[Dict[str, Any]] = []
    for term_obj in data.get("Terms", []):
        start = term_obj["Index"]
        matched_text = term_obj["MatchedText"]
        end = start + len(matched_text)
        confidence = 0.0
        term_matches = term_obj.get("TermMatches", [])
        if term_matches:
            confidence = max(tm["Confidence"] for tm in term_matches)
        spans.append(
            {
                "start": start,
                "end": end,
                "category": term_obj["Term"],
                "score": confidence,
            }
        )
    redacted_chars = list(text)
    for span in sorted(spans, key=lambda s: s["start"], reverse=True):
        for pos in range(span["start"], span["end"]):
            redacted_chars[pos] = "*"
    redacted_text = "".join(redacted_chars)
    return {"original_text": text, "redacted_text": redacted_text, "spans": spans}
