import requests
from speech_models import TranscriptionResult, TranscriptSegment
from typing import List


def moderate_transcript(transcript: TranscriptionResult) -> List[TranscriptSegment]:
    """
    Moderates transcript text before publishing using Perspective API.

    Args:
        transcript: TranscriptionResult containing segments to moderate.

    Returns:
        List of TranscriptSegment objects with moderation flags.
    """
    api_key = "PERSPECTIVE_API_KEY"  # Replace with environment variable in production
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    moderated_segments = []
    for segment in transcript.segments:
        payload = {
            "comment": {"text": segment.text},
            "requestedAttributes": {
                "TOXICITY": {},
                "PROFANITY": {},
                "INSULT": {},
            },
            "languages": [transcript.language_code],
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        attributes = response.json().get("attributeScores", {})

        # Add moderation flags to segment
        segment_dict = segment.__dict__
        segment_dict["moderation"] = {
            "toxicity": attributes.get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0),
            "profanity": attributes.get("PROFANITY", {})
            .get("summaryScore", {})
            .get("value", 0),
            "insult": attributes.get("INSULT", {})
            .get("summaryScore", {})
            .get("value", 0),
        }

        moderated_segments.append(TranscriptSegment(**segment_dict))

    return moderated_segments
