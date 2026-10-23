import os
from typing import Optional
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client, build_recognition_config, build_recognition_audio
from speech_models import TranscriptionRequest

def submit_timestamped_transcription(request: TranscriptionRequest) -> Optional[str]:
    # Ensure word time offsets are requested
    request.enable_word_time_offsets = True

    client = get_speech_client()

    config = build_recognition_config(
        diarization_enabled=request.diarization_enabled,
        enable_word_time_offsets=request.enable_word_time_offsets,
        language_code=request.language_code
    )
    audio = build_recognition_audio(request.gcs_uri)

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name