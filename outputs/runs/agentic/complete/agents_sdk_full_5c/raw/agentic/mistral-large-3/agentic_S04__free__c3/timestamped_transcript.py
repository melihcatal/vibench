from google.cloud import speech_v2 as speech
from speech_client import get_speech_client
from speech_models import TimestampedTranscriptResult

def timestamped_transcript(operation_name: str) -> TimestampedTranscriptResult:
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return TimestampedTranscriptResult(status="PROCESSING", segments=[])

    segments = []
    for uri, result in operation.result().results.items():
        for alternative in result.alternatives:
            for word in alternative.words:
                segments.append({
                    "word": word.word,
                    "start_time": word.start_offset.total_seconds(),
                    "end_time": word.end_offset.total_seconds(),
                })

    return TimestampedTranscriptResult(status="COMPLETED", segments=segments)