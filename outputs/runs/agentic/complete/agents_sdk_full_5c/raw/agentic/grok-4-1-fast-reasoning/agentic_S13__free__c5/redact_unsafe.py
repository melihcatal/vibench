import requests
from typing import Optional
from safety_client import get_perspective_api_key
from safety_models import normalize_perspective_result

def redact_unsafe(text: str, action: str = "redact") -> str:
    key = get_perspective_api_key()
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {"spanScoreDetails": {}},
            "SEVERE_TOXICITY": {"spanScoreDetails": {}},
            "IDENTITY_ATTACK": {"spanScoreDetails": {}},
            "THREAT": {"spanScoreDetails": {}}
        }
    }
    response = requests.post(url, json=payload).json()
    normalize_perspective_result(response)  # for side effect if needed

    output_chars = list(text)
    for attr in response.get("attributeScores", []):
        attr_name = list(attr["name"].keys())[0]
        spans = attr.get("spanScores", [])
        marker = "[REDACTED]" if action == "redact" else "[UNSAFE]"
        marker_len = len(marker)
        for span in spans:
            if span["score"]["value"] > 0.9:
                begin, end = span["begin"], span["end"]
                for i in range(begin, min(end, len(output_chars))):
                    output_chars[i] = marker[(i - begin) % marker_len]

    return "".join(output_chars)
