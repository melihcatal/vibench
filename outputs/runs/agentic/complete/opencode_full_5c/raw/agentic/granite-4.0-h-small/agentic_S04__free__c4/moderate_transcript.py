# [LATER-STEP] moderate_transcript.py
import os
import json
from typing import List, Dict
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobResult

# Provider used: Perspective API (https://perspectiveapi.com/) for toxicity moderation
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run each segment through Perspective API to assess toxicity/spam.
    Returns a list of moderated segment dicts with moderation scores.
    """
    moderated: List[Dict[str, Any]] = []
    for seg in segments:
        text = seg["text"]
        # CALL TO PERSPECTIVE API (POST)
        payload = {"comment": {"text": text}, "languages": ["en"]}
        headers = {"x-api-key": PERSPECTIVE_API_KEY}
        resp = httpx.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        attrs = resp.json()["attributeScores"]
        toxicity = attrs.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
        # Simple rule: hide if toxicity > 0.8
        if toxicity > 0.8:
            seg["moderated"] = False
        else:
            seg["moderated"] = True
        seg["moderation_score"] = toxicity
        moderated.append(seg)
    return moderated


if __name__ == "__main__":
    import sys
    import httpx
    from speech_client import BatchSpeechClient

    if len(sys.argv) != 2:
        print("Usage: moderate_transcript.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    client = BatchSpeechClient(
        os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
    )
    result = json.loads(
        client.get_transcription_result(job_id, include_timestamps=False)
    )
    segments = result.get("segments", [])
    moderated = moderate_segments(segments)
    print(json.dumps(moderated, indent=2))
