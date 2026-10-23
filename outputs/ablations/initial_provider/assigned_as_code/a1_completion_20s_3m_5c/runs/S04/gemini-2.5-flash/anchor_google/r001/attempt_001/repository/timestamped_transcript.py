from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_recognition_config, create_recognition_audio

def timestamped_transcript(payload: dict, config: dict = None):
    config = config or {}
    client = get_speech_client()

    recognition_config = create_recognition_config(
        language_code=payload["language_code"],
        enable_word_time_offsets=True,
    )
    audio = create_recognition_audio(payload["audio_uri"])

    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(**recognition_config),
        audio=speech.RecognitionAudio(**audio),
    )

    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }
