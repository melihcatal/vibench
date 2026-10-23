from typing import Dict, List

from speech_models import normalize_transcript


def handle_partial_results(events: List[Dict[str, object]]) -> List[str]:
    outputs: List[str] = []
    for event in events:
        transcript = normalize_transcript(event)
        if transcript.text:
            outputs.append(transcript.text if not transcript.is_final else f"FINAL: {transcript.text}")
    return outputs
