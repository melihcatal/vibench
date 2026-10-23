from typing import Any, Dict

from speech_models import normalize_transcript


def handle_partial_and_final(event: Any) -> Dict[str, Any]:
    transcript = normalize_transcript(event)
    return {
        "text": transcript.text,
        "is_final": transcript.is_final,
        "confidence": transcript.confidence,
    }
