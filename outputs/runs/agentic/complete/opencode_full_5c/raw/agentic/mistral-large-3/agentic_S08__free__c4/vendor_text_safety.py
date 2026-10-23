from typing import Optional
import requests
import os


def moderate_vendor_notes(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        return {"is_safe": True, "flags": []}

    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    flags = []
    for attribute, details in result["attributeScores"].items():
        score = details["summaryScore"]["value"]
        if score > 0.7:
            flags.append(attribute.lower())

    return {
        "is_safe": len(flags) == 0,
        "flags": flags,
        "scores": {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in result["attributeScores"]
        },
    }
