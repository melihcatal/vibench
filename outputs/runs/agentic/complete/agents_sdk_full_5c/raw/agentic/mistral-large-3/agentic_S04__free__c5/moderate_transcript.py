import requests
from typing import List
from speech_models import TranscriptSegment

def moderate_transcript(segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
    """Moderate transcript text before publishing using Perspective API."""
    api_key = "YOUR_PERSPECTIVE_API_KEY"
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    moderated_segments = []
    for segment in segments:
        payload = {
            "comment": {"text": segment.text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"]
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            if toxicity_score < 0.7:
                moderated_segments.append(segment)
        else:
            raise RuntimeError("Failed to moderate transcript segment.")
    
    return moderated_segments