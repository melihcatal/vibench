import os
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from speech_client import get_speech_client
from speech_models import TranscriptionRequest, TranscriptionResponse

def submit_transcription(audio_uri: str, language_code: str = "en-US") -> TranscriptionResponse:
    """
    Submits an audio file for batch transcription using Google Cloud Speech-to-Text.
    """
    client = get_speech_client()
    request = TranscriptionRequest(
        audio_uri=audio_uri,
        language_code=language_code,
        config={
            "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "sample_rate_hertz": 16000,
            "language_code": language_code,
            "enable_automatic_punctuation": True,
            "model": "latest_long",
        }
    )

    try:
        operation = client.long_running_recognize(
            request={
                "config": request.config,
                "audio": {"uri": request.audio_uri},
            }
        )
        return TranscriptionResponse(
            job_id=operation.operation.name,
            status="SUBMITTED",
            transcript=None,
            error=None
        )
    except GoogleAPICallError as e:
        return TranscriptionResponse(
            job_id=None,
            status="FAILED",
            transcript=None,
            error=str(e)
        )