import os
import requests
import json


def moderate_transcript(transcript_text):
    """Moderate transcript text before publishing using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": transcript_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()

        result = response.json()

        scores = {}
        if "attributeScores" in result:
            for attr_name, attr_data in result["attributeScores"].items():
                scores[attr_name] = {
                    "score": attr_data["summaryScore"]["value"],
                    "type": attr_data["summaryScore"]["type"],
                }

        # Determine if content needs moderation
        needs_moderation = any(
            score_data["score"] > 0.7 for score_data in scores.values()
        )

        return {
            "text": transcript_text,
            "scores": scores,
            "needs_moderation": needs_moderation,
            "provider": "Perspective API",
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e), "provider": "Perspective API"}


def moderate_segments(segments):
    """Moderate multiple transcript segments."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    moderated_results = []

    for i, segment in enumerate(segments):
        if isinstance(segment, dict):
            text = segment.get("text", "")
        else:
            text = str(segment)

        result = moderate_transcript(text)
        result["segment_index"] = i
        moderated_results.append(result)

    # Overall assessment
    any_needs_moderation = any(
        result.get("needs_moderation", False)
        for result in moderated_results
        if isinstance(result, dict)
    )

    return {
        "segments": moderated_results,
        "overall_needs_moderation": any_needs_moderation,
        "provider": "Perspective API",
    }
