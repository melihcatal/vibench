from google.cloud import speech_v1
from speech_client import get_speech_client
from speech_models import TimestampedWord


def timestamped_transcript(operation_name):
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = get_speech_client()

    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return None

    response = speech_v1.LongRunningRecognizeResponse.deserialize(
        operation.response.value
    )

    timestamped_words = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                timestamped_words.append(
                    TimestampedWord(
                        word=word_info.word,
                        start_time=word_info.start_time.total_seconds(),
                        end_time=word_info.end_time.total_seconds(),
                        confidence=alternative.confidence,
                    )
                )

    return timestamped_words
