"""Moderate transcript text before publishing using Perspective API."""

import os
from typing import Dict, List, Optional

import requests

from speech_models import TranscriptionResponse, TranscriptSegment


PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_PERSPECTIVE_ATTRIBUTES = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY"]


def create_perspective_client(api_key: Optional[str] = None) -> dict:
    """Return a configured session dict for Perspective API calls.

    Args:
        api_key: Perspective API key; falls back to PERSPECTIVE_API_KEY env var.

    Returns:
        Dict containing the base URL and API key for requests.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")
    return {
        "endpoint": PERSPECTIVE_API_ENDPOINT,
        "api_key": api_key,
    }


def analyze_text_moderation(
    text: str,
    attributes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    language: str = "en",
) -> Dict:
    """Analyze a single text segment using Perspective API.

    Args:
        text: The text to moderate.
        attributes: List of Perspective API attributes to evaluate.
        api_key: Optional API key for Perspective API.
        language: Language code for analysis.

    Returns:
        Dict of attribute scores from the Perspective API.
    """
    client = create_perspective_client(api_key)
    if attributes is None:
        attributes = DEFAULT_PERSPECTIVE_ATTRIBUTES

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": [language],
        "spanAnnotations": True,
    }

    response = requests.post(
        client["endpoint"],
        params={"key": client["api_key"]},
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()


def moderate_transcript(
    response: TranscriptionResponse,
    threshold: float = 0.7,
    attributes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """Moderate all segments of a transcript using Perspective API.

    Args:
        response: TranscriptionResponse to moderate.
        threshold: Score above which content is flagged.
        attributes: Perspective API attributes to check.
        api_key: Optional Perspective API key.

    Returns:
        Dict with overall moderation results and flagged segments.
    """
    results = {
        "job_id": response.job_id,
        "total_segments": len(response.segments),
        "flagged_segments": [],
        "overall_risk": "low",
        "max_toxicity_score": 0.0,
    }

    for seg in response.segments:
        if not seg.text:
            continue
        try:
            analysis = analyze_text_moderation(seg.text, attributes=attributes, api_key=api_key)
            scores = analysis.get("attributeScores", {})
            max_score = 0.0
            flagged_attrs = []
            for attr_name, attr_data in scores.items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                if score > max_score:
                    max_score = score
                if score > threshold:
                    flagged_attrs.append(attr_name)

            if max_score > results["max_toxicity_score"]:
                results["max_toxicity_score"] = max_score

            if flagged_attrs:
                results["flagged_segments"].append({
                    "text": seg.text,
                    "start_ms": seg.start_ms,
                    "end_ms": seg.end_ms,
                    "speaker": seg.speaker,
                    "flagged_attributes": flagged_attrs,
                    "max_score": max_score,
                })
        except requests.RequestException as e:
            print(f"Moderation request failed for segment: {e}")
            continue

    if results["max_toxicity_score"] > 0.9:
        results["overall_risk"] = "high"
    elif results["max_toxicity_score"] > threshold:
        results["overall_risk"] = "medium"

    return results


def filter_safe_segments(
    response: TranscriptionResponse,
    threshold: float = 0.7,
    api_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Return only safe segments from a transcript after moderation.

    Args:
        response: TranscriptionResponse to filter.
        threshold: Score above which segments are excluded.
        api_key: Optional Perspective API key.

    Returns:
        New TranscriptionResponse with only safe segments.
    """
    safe_segments = []
    for seg in response.segments:
        if not seg.text:
            safe_segments.append(seg)
            continue
        try:
            analysis = analyze_text_moderation(seg.text, api_key=api_key)
            scores = analysis.get("attributeScores", {})
            max_score = max(
                (attr.get("summaryScore", {}).get("value", 0.0) for attr in scores.values()),
                default=0.0,
            )
            if max_score <= threshold:
                safe_segments.append(seg)
        except requests.RequestException:
            safe_segments.append(seg)

    return TranscriptionResponse(
        job_id=response.job_id,
        text=" ".join(s.text for s in safe_segments),
        segments=safe_segments,
        words=response.words,
        language=response.language,
        audio_duration_ms=response.audio_duration_ms,
        status=response.status,
    )


if __name__ == "__main__":
    from speech_models import TranscriptionResponse, TranscriptSegment
    demo = TranscriptionResponse(
        job_id="mod-demo",
        text="This is a sample transcript for moderation testing.",
        segments=[
            TranscriptSegment(text="This is a sample transcript", start_ms=0, end_ms=2000),
            TranscriptSegment(text="for moderation testing", start_ms=2000, end_ms=4000),
        ],
    )
    print("Moderation requires PERSPECTIVE_API_KEY to be set.")
