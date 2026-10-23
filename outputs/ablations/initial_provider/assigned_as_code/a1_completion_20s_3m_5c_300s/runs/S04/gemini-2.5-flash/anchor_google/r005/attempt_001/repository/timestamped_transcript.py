from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionRequest, TranscriptionJob

def timestamped_transcript(request: TranscriptionRequest) -> TranscriptionJob:
    client = get_speech_client()

    config = speech.RecognitionConfig(
        language_code=request.language_code,
        enable_word_time_offsets=True,
    )
    audio = speech.RecognitionAudio(uri=request.audio_uri)

    operation = client.long_running_recognize(config=config, audio=audio)

    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }
