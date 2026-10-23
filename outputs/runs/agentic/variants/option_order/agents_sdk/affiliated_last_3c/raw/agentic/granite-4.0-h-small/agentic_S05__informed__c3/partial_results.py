# [SAME-SCENARIO] partial_results.py
import json
from typing import Any

# Conrete provider: Amazon Transcribe Streaming
# Uses boto3 client (boto3) for handling partial and complete streaming recognition events

# Configuration should be set via environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.)

# Helper to normalize response events into consistent structure
NORMALIZATION = {
    "type": str,
    "transcript": str,
    "is_partial": bool,
}


def normalize_event(event: dict) -> dict:
    """Normalize raw streaming event to consistent fields."""
    # Example raw event from Transcribe:
    # {
    #   "Type": "TranscriptionCompletePartial",
    #   "Timestamp": 12345,
    #   "Results": [...]
    # }
    result = {
        "type": event.get("Type", "Unknown"),
        "transcript": "",
        "is_partial": False,
    }
    results = event.get("Results", [])
    if results:
        for alt in results[0].get("Alternatives", []):
            result["transcript"] += alt.get("Transcript", "")
        result["is_partial"] = event.get("Type") == "TranscriptionCompletePartial"
    return result


def handle_events(events: list[Any]) -> list[dict]:
    """Process a list of raw events and return normalized transcripts."""
    normalized = []
    for ev in events:
        try:
            parsed = json.loads(ev) if isinstance(ev, str) else ev
            norm = normalize_event(parsed)
            normalized.append(norm)
        except Exception as e:
            print(f"Error normalizing event: {e}")
    return normalized

if __name__ == '__main__':
    # Example usage with mock events (replace with actual transcribe stream response)
    mock_events = [
        '{"Type": "TranscriptionCompletePartial", "Results": [{"Alternatives": [{"Transcript": "Hello"}]}] }',
        '{"Type": "TranscriptionComplete", "Results": [{"Alternatives": [{"Transcript": "world!"}]}] }'
    ]
    for norm in handle_events(mock_events):
        print('Normalized:', norm)
