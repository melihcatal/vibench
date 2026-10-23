from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_models import SpeechModels, TranscriptionResult, WordInfo
from typing import List, Dict


def timestamped_transcript(operation_name: str) -> List[Dict[str, Any]]:
    """Return word-level timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    operation = client.transport._operations_client.get_operation(operation_name)
    if not operation.done:
        raise ValueError("Transcription job is not yet complete.")

    response = types.LongRunningRecognizeResponse.from_json(operation.response)
    result = SpeechModels.normalize_response(response)

    return [
        {
            "word": word.word,
            "start_time": word.start_time,
            "end_time": word.end_time,
            "speaker_tag": word.speaker_tag,
        }
        for word in result.words
    ]
