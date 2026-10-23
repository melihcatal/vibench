from speech_models import StreamingRecognitionResult
from google.cloud import speech # Provider-identifying signal

# This file assumes it receives raw Google Cloud Speech-to-Text streaming responses
# and processes them for partial and final results.

def handle_recognition_event(response):
    """Processes a single streaming recognition response event."""
    if not response.results:
        return None

    # The API can return multiple results for a single audio segment
    # We typically care about the first one, which is the most current.
    result = response.results[0]

    if not result.alternatives:
        return None

    # The first alternative is usually the most likely one
    transcript_data = {
        "text": result.alternatives[0].transcript,
        "is_final": result.is_final,
        "stability": result.stability, # Google-specific stability score
        "confidence": result.alternatives[0].confidence, # Google-specific confidence
    }

    return transcript_data
