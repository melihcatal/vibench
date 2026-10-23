from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import SpeechResponseParser, TranscriptionResult
from typing import List, Dict
import time


def timestamped_transcript(audio_uri: str) -> List[Dict[str, Any]]:
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    config = TranscriptionConfig(
        language_code="en-US",
        model="latest_long",
        use_enhanced=True,
        enable_word_time_offsets=True,
    )
    client = SpeechClient(config)
    operation_name = client.submit_transcription(audio_uri)

    operation = client.client.transport._operations_client.get_operation(operation_name)
    while not operation.done:
        time.sleep(10)
        operation = client.client.transport._operations_client.get_operation(
            operation_name
        )

    if operation.response:
        response = types.LongRunningRecognizeResponse.from_json(operation.response)
        result = SpeechResponseParser.parse_transcription_response(response)
        return [
            {
                "word": word.word,
                "start_time": word.start_time,
                "end_time": word.end_time,
                "speaker_tag": word.speaker_tag,
            }
            for word in result.words
        ]
    else:
        raise ValueError(f"Timestamp extraction failed: {operation.metadata}")
