import os
import requests
from translation_models import TranslationResponse


PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def check_unsafe_copy(
    translations: list[TranslationResponse],
    attributes: list[str] | None = None,
    language: str = "en",
    threshold: float = 0.5,
) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable is required for Perspective API access"
        )

    if attributes is None:
        attributes = DEFAULT_ATTRIBUTES

    results = []
    flagged_segments = []

    for translation in translations:
        for result in translation.results:
            text = result.text
            payload = {
                "comment": {"text": text},
                "languages": [language],
                "requestedAttributes": {attr: {} for attr in attributes},
            }

            response = requests.post(
                PERSPECTIVE_API_ENDPOINT,
                params={"key": api_key},
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            analysis = response.json()

            attribute_scores = {}
            is_flagged = False
            flagged_attributes = []

            for attr_name, attr_data in analysis.get("attributeScores", {}).items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                attribute_scores[attr_name] = round(score, 4)
                if score >= threshold:
                    is_flagged = True
                    flagged_attributes.append(
                        {
                            "attribute": attr_name,
                            "score": score,
                            "threshold": threshold,
                        }
                    )

            segment_result = {
                "text_preview": text[:100] + ("..." if len(text) > 100 else ""),
                "attribute_scores": attribute_scores,
                "is_flagged": is_flagged,
                "flagged_attributes": flagged_attributes,
                "source_lang": translation.source_lang,
                "target_lang": translation.target_lang,
            }
            results.append(segment_result)

            if is_flagged:
                flagged_segments.append(segment_result)

    return {
        "total_segments_checked": len(results),
        "flagged_count": len(flagged_segments),
        "threshold_used": threshold,
        "attributes_checked": attributes,
        "service": "Perspective API",
        "results": results,
        "flagged_segments": flagged_segments,
    }
