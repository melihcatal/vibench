"""
[LATER-STEP] Moderate transcript text before publishing via Perspective API.

Uses Google's Perspective API to analyze transcript segments for toxicity,
severe toxicity, identity attack, profanity, and other safety attributes.
Provider: Perspective API
SDK: requests
Auth: PERSPECTIVE_API_KEY
"""

import os
import json
from typing import List, Optional, Dict, Any

import requests

from speech_models import TranscriptResponse, Utterance


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_HOST = "commentanalyzer.googleapis.com"


def get_perspective_api_key(api_key: Optional[str] = None) -> str:
    """
    Retrieve the Perspective API key from parameter or environment.

    Args:
        api_key: Optional API key. Falls back to PERSPECTIVE_API_KEY env var.

    Returns:
        Perspective API key string.

    Raises:
        ValueError: If no API key is found.
    """
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError(
            "Perspective API key not found. Set PERSPECTIVE_API_KEY environment variable or pass api_key."
        )
    return key


def analyze_text(
    text: str,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    span_annotations: bool = False,
) -> Dict[str, Any]:
    """
    Analyze a single text string with Perspective API.

    Args:
        text: Text to analyze for safety attributes.
        attributes: List of attributes to score. Defaults include
            TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, PROFANITY.
        languages: List of language codes. Defaults to ['en'].
        api_key: Perspective API key.
        span_annotations: Whether to include span annotations.

    Returns:
        Dictionary with attribute scores from Perspective API.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    key = get_perspective_api_key(api_key)

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "PROFANITY",
            "INSULT",
            "THREAT",
            "SEXUALLY_EXPLICIT",
            "FLIRTATION",
        ]

    if languages is None:
        languages = ["en"]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "spanAnnotations": span_annotations,
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
    )
    response.raise_for_status()

    return response.json()


def moderate_transcript(
    transcript: TranscriptResponse,
    threshold: float = 0.7,
    attributes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate all utterances in a transcript using Perspective API.

    Analyzes each utterance for toxic content and flags segments
    exceeding the safety threshold.

    Args:
        transcript: Normalized TranscriptResponse to moderate.
        threshold: Score threshold above which text is flagged (0.0-1.0).
        attributes: Perspective API attributes to check.
        api_key: Perspective API key.

    Returns:
        Dictionary with moderation results including flagged segments,
        overall safety score, and per-utterance analysis.
    """
    results = {
        "transcript_id": transcript.transcript_id,
        "total_utterances": len(transcript.utterances),
        "flagged_utterances": [],
        "safe_utterances": [],
        "overall_safe": True,
        "attribute_scores": {},
    }

    for i, utterance in enumerate(transcript.utterances):
        if not utterance.text.strip():
            results["safe_utterances"].append(i)
            continue

        analysis = analyze_text(
            text=utterance.text,
            attributes=attributes,
            api_key=api_key,
        )

        attribute_scores = analysis.get("attributeScores", {})
        utterance_flagged = False
        utterance_max_score = 0.0

        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            if score > threshold:
                utterance_flagged = True
                results["overall_safe"] = False
            utterance_max_score = max(utterance_max_score, score)

        if utterance_flagged:
            results["flagged_utterances"].append({
                "utterance_index": i,
                "speaker": utterance.speaker,
                "text": utterance.text,
                "max_score": utterance_max_score,
                "scores": {
                    attr_name: attr_data.get("summaryScore", {}).get("value", 0.0)
                    for attr_name, attr_data in attribute_scores.items()
                },
            })
        else:
            results["safe_utterances"].append(i)

        # Aggregate attribute scores
        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            if attr_name not in results["attribute_scores"]:
                results["attribute_scores"][attr_name] = []
            results["attribute_scores"][attr_name].append(score)

    # Compute averages for attribute scores
    for attr_name, scores in results["attribute_scores"].items():
        results["attribute_scores"][attr_name] = sum(scores) / len(scores) if scores else 0.0

    return results


def moderate_full_text(
    text: str,
    threshold: float = 0.7,
    attributes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate a single block of text with Perspective API.

    Args:
        text: Text to moderate.
        threshold: Score threshold for flagging.
        attributes: Attributes to check.
        api_key: Perspective API key.

    Returns:
        Moderation results with attribute scores.
    """
    analysis = analyze_text(
        text=text,
        attributes=attributes,
        api_key=api_key,
    )

    attribute_scores = analysis.get("attributeScores", {})
    flagged = False
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score > threshold:
            flagged = True

    return {
        "text": text,
        "flagged": flagged,
        "max_score": max(scores.values()) if scores else 0.0,
        "scores": scores,
    }


def filter_safe_transcript(
    transcript: TranscriptResponse,
    moderation_results: Dict[str, Any],
    replacement_text: str = "[FLAGGED]",
) -> TranscriptResponse:
    """
    Create a cleaned transcript with flagged content replaced.

    Args:
        transcript: Original transcript.
        moderation_results: Results from moderate_transcript().
        replacement_text: Text to substitute for flagged content.

    Returns:
        New TranscriptResponse with flagged utterances replaced.
    """
    flagged_indices = set(
        item["utterance_index"] for item in moderation_results.get("flagged_utterances", [])
    )

    safe_utterances = []
    for i, utterance in enumerate(transcript.utterances):
        if i in flagged_indices:
            safe_utterance = Utterance(
                speaker=utterance.speaker,
                text=replacement_text,
                words=utterance.words,
                start_ms=utterance.start_ms,
                end_ms=utterance.end_ms,
                confidence=utterance.confidence,
                sentiment=utterance.sentiment,
            )
        else:
            safe_utterance = utterance
        safe_utterances.append(safe_utterance)

    safe_text = "\n".join(
        u.text for u in safe_utterances if u.text != replacement_text
    )

    safe_response = TranscriptResponse(
        transcript_id=transcript.transcript_id,
        audio_url=transcript.audio_url,
        full_text=safe_text,
        utterances=safe_utterances,
        words=transcript.words,
        status=transcript.status,
        language_code=transcript.language_code,
        duration_ms=transcript.duration_ms,
        created_at=transcript.created_at,
    )

    return safe_response


def main():
    """CLI entry point for moderating a transcript."""
    import argparse

    parser = argparse.ArgumentParser(description="Moderate transcript with Perspective API")
    parser.add_argument("transcript_id", help="Transcript ID to moderate")
    parser.add_argument("--threshold", type=float, default=0.7, help="Flag threshold (0.0-1.0)")
    parser.add_argument("--filter", action="store_true", help="Output cleaned transcript")

    args = parser.parse_args()

    from poll_transcription import poll_transcription

    transcript = poll_transcription(args.transcript_id)

    results = moderate_transcript(
        transcript=transcript,
        threshold=args.threshold,
    )

    if args.filter and not results["overall_safe"]:
        safe_transcript = filter_safe_transcript(transcript, results)
        print("=== Cleaned Transcript ===")
        print(safe_transcript.full_text)
    else:
        print("=== Moderation Results ===")
        print(f"Overall safe: {results['overall_safe']}")
        print(f"Flagged utterances: {len(results['flagged_utterances'])}/{results['total_utterances']}")
        print(f"Average scores:")
        for attr, score in results["attribute_scores"].items():
            print(f"  {attr}: {score:.3f}")

    return results


if __name__ == "__main__":
    main()
