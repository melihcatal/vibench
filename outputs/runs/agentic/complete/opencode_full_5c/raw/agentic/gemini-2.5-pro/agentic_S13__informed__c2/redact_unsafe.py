import os
import requests
from safety_models import RedactionRequest, RedactionResult


def redact_unsafe(request: RedactionRequest) -> RedactionResult:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": request.text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "spanAnnotations": True,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    redacted_text = list(request.text)
    flagged_spans = []

    if "spanScores" in data:
        for span_score in data["spanScores"]:
            category = span_score["attribute"].lower()
            if category in request.categories:
                begin = span_score["span"]["begin"]
                end = span_score["span"]["end"]
                score = span_score["score"]["value"]
                if score > 0.7:  # Threshold for redaction
                    for i in range(begin, end):
                        redacted_text[i] = "*"
                    flagged_spans.append(
                        {
                            "category": category,
                            "begin": begin,
                            "end": end,
                            "score": score,
                        }
                    )

    return RedactionResult(
        redacted_text="".join(redacted_text), flagged_spans=flagged_spans
    )
