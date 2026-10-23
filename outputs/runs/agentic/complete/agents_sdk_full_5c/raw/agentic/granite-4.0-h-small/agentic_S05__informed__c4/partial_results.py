# [SAME-SCENARIO] partial_results.py
# Handles partial and final streaming recognition results using Google Cloud Speech-to-Text
import json
from typing import Any, Dict

# Provider identifier
PROVIDER = "google"

SERVER_TIMESTAMP_KEY = "content"
INTERIM_FIELD = "alternatives"

 def parse_speech_response(response: bytes) -> Dict[str, Any]:
    """Parse a protobuf response from Google Speech streaming API."""
    # NOTE: In real code you would use the google-cloud-speech library to parse.
    # Here we simulate parsing with a placeholder JSON conversion.
    # The actual response bytes contain binary protobuf data.
    try:
        # Placeholder: convert bytes to dict (actual implementation omitted)
        return json.loads(response.decode("utf-8"))
    except Exception:
        # Fallback when response cannot be decoded
        return {}

 def handle_recognition_event(event: Dict[str, Any]) -> None:
    """Print interim or final transcript fragments."""
    results = event.get(INTERIM_FIELD, [])
    for alt in results:
        if alt.get("words", []):  # non-empty hypothesis
            transcript = alt["transcript"]
            is_final = alt.get("is_final", False)
            if is_final:
                print(f"[FINAL] {transcript}")
            else:
                print(f"[INTERIM] {transcript}")

if __name__ == "__main__":
    # Example dummy response (replace with real protobuf parsing in production)
    dummy_response = b'{"alternatives":[{"transcript":"hello","is_final":false}],"content":""}'
    event = parse_speech_response(dummy_response)
    handle_recognition_event(event)