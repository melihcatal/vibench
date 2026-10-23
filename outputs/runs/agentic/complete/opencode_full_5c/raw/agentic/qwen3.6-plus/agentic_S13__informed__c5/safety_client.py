import os
import requests
from typing import Optional

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")
    return api_key


def build_perspective_payload(
    text: str,
    languages: Optional[list[str]] = None,
    attributes: Optional[list[str]] = None,
    score_threshold: float = 0.0,
) -> dict:
    if languages is None:
        languages = ["en"]
    if attributes is None:
        attributes = PERSPECTIVE_ATTRIBUTES

    return {
        "comment": {"text": text},
        "languages": languages,
        "requestedAttributes": {
            attr: {"scoreType": "PROBABILITY", "scoreThreshold": score_threshold}
            for attr in attributes
        },
        "spanAnnotations": True,
        "doNotStore": True,
    }


def call_perspective_api(
    text: str,
    languages: Optional[list[str]] = None,
    attributes: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict:
    if api_key is None:
        api_key = get_perspective_api_key()

    payload = build_perspective_payload(text, languages, attributes)

    response = requests.post(
        PERSPECTIVE_API_BASE_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def parse_perspective_scores(raw_response: dict) -> dict[str, float]:
    attribute_scores = raw_response.get("attributeScores", {})
    scores = {}
    for attr_name, attr_data in attribute_scores.items():
        summary_score = attr_data.get("summaryScore", {})
        scores[attr_name] = summary_score.get("value", 0.0)
    return scores


def parse_perspective_spans(raw_response: dict) -> dict[str, list[dict]]:
    attribute_scores = raw_response.get("attributeScores", {})
    spans_by_category = {}
    for attr_name, attr_data in attribute_scores.items():
        span_scores = attr_data.get("spanScores", [])
        spans = []
        for entry in span_scores:
            span = entry.get("span", {})
            spans.append(
                {
                    "begin": span.get("begin", 0),
                    "end": span.get("end", 0),
                    "score": entry.get("score", {}).get("value", 0.0),
                }
            )
        if spans:
            spans_by_category[attr_name] = spans
    return spans_by_category


def normalize_category_name(attr_name: str) -> str:
    return attr_name.replace("_", " ").title()
