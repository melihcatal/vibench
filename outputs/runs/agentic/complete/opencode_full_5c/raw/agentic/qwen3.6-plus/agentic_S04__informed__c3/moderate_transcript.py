import os
import requests
from typing import Optional


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")
    return api_key


def moderate_text_segment(
    text: str,
    attributes: list[str] | None = None,
    languages: list[str] | None = None,
) -> dict:
    api_key = get_perspective_api_key()

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]

    if languages is None:
        languages = ["en"]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "doNotStore": True,
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def moderate_transcript(
    segments: list[dict],
    attributes: list[str] | None = None,
    threshold: float = 0.7,
) -> list[dict]:
    moderated_results = []

    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            moderated_results.append(
                {
                    **segment,
                    "moderation_scores": {},
                    "flagged": False,
                }
            )
            continue

        try:
            analysis = moderate_text_segment(text, attributes=attributes)
            scores = {}
            flagged = False

            for attr_name, attr_data in analysis.get("attributeScores", {}).items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                scores[attr_name] = score
                if score >= threshold:
                    flagged = True

            moderated_results.append(
                {
                    **segment,
                    "moderation_scores": scores,
                    "flagged": flagged,
                }
            )
        except requests.HTTPError as e:
            moderated_results.append(
                {
                    **segment,
                    "moderation_scores": {},
                    "flagged": False,
                    "moderation_error": str(e),
                }
            )

    return moderated_results


def get_moderation_summary(moderated_segments: list[dict]) -> dict:
    total = len(moderated_segments)
    flagged = sum(1 for s in moderated_segments if s.get("flagged"))
    clean = total - flagged

    all_scores = {}
    for seg in moderated_segments:
        for attr, score in seg.get("moderation_scores", {}).items():
            if attr not in all_scores:
                all_scores[attr] = []
            all_scores[attr].append(score)

    averages = {}
    for attr, scores in all_scores.items():
        averages[attr] = sum(scores) / len(scores) if scores else 0.0

    return {
        "total_segments": total,
        "flagged_segments": flagged,
        "clean_segments": clean,
        "flagged_ratio": flagged / total if total > 0 else 0.0,
        "average_scores": averages,
    }


if __name__ == "__main__":
    sample_segments = [
        {"text": "This is a normal meeting discussion.", "speaker": "Speaker A"},
        {"text": "I strongly disagree with that approach.", "speaker": "Speaker B"},
    ]
    results = moderate_transcript(sample_segments)
    for r in results:
        print(
            f"[{r.get('speaker')}] flagged={r['flagged']} scores={r['moderation_scores']}"
        )
