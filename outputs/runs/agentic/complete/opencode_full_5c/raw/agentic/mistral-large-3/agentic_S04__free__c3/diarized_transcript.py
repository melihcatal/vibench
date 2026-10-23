from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import TranscriptionConfig, SpeechResponseParser
from typing import List, Dict


def diarized_transcript(audio_uri: str) -> List[Dict[str, Any]]:
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    diarization_config = types.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )
    config = TranscriptionConfig(
        language_code="en-US",
        model="latest_long",
        use_enhanced=True,
        diarization_config=diarization_config,
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
                "speaker": segment.speaker_tag,
                "text": segment.text,
                "start_time": segment.start_time,
                "end_time": segment.end_time,
            }
            for segment in result.segments
        ]
    else:
        raise ValueError(f"Diarization failed: {operation.metadata}")
