from google.cloud.speech import StreamingRecognizeResponse
from speech_models import TranscriptSegment


def handle_recognition_event(response: StreamingRecognizeResponse):
    """Handles a streaming recognition event and returns TranscriptSegments."""
    if not response.results:
        return []

    segments = []
    for result in response.results:
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]
        segment = TranscriptSegment(
            text=alternative.transcript,
            is_final=result.is_final,
            stability=result.stability,
            language_code=result.language_code or "en-US",
        )
        segments.append(segment)
    return segments
