from __future__ import annotations

from messaging_client import comprehend_client
from messaging_models import normalize_text_payload


def check_message_safety(message: dict) -> dict[str, object]:
    text = normalize_text_payload(message)
    response = comprehend_client().detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode="en",
    )
    result = response["ResultList"][0]
    labels = result.get("Labels", [])
    unsafe = any(label.get("Score", 0.0) >= 0.7 for label in labels)
    return {
        "provider": "aws_comprehend",
        "unsafe": unsafe,
        "labels": [
            {"name": label.get("Name", ""), "score": label.get("Score", 0.0)}
            for label in labels
        ],
        "text": text,
    }
