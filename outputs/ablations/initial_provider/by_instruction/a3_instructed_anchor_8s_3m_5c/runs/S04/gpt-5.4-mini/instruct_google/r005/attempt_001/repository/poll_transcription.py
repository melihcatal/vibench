from speech_client import get_client
from speech_models import normalize_segments, normalize_words


def poll_transcription(operation):
    result = operation.result()
    alternative = result.results[0].alternatives[0] if result.results else None
    return {
        "text": alternative.transcript if alternative else "",
        "segments": normalize_segments(result.results),
        "words": normalize_words(alternative.words if alternative else []),
    }
