from google.cloud import speech

from speech_client import get_client
from speech_models import build_recognition_config, normalize_transcript_response


def diarized_transcript(payload, config=None):
    client = get_client(config)
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(**build_recognition_config({**payload, "enable_speaker_diarization": True})),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    response = operation.result()
    return {
        "job_id": operation.operation.name,
        "status": "COMPLETED",
        "transcript": normalize_transcript_response(response),
    }
