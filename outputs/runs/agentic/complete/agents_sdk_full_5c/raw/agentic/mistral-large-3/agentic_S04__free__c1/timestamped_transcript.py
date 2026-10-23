from google.cloud import speech_v2 as speech
from typing import List, Dict
from speech_client import get_speech_client
from speech_models import TimestampedWord

def timestamped_transcript(operation_name: str) -> List[TimestampedWord]:
    """Returns word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done or not operation.response:
        raise ValueError("Transcription not completed or no response available")

    words = []
    for result in operation.response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                words.append(
                    TimestampedWord(
                        word=word_info.word,
                        start_time=word_info.start_offset.total_seconds(),
                        end_time=word_info.end_offset.total_seconds(),
                    )
                )
    return words