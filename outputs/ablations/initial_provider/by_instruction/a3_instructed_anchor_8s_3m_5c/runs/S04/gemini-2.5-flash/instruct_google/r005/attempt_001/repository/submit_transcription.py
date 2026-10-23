from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from speech_client import get_speech_client
from speech_models import TranscriptionRequest

def submit_transcription_job(request: TranscriptionRequest):
    client = get_speech_client()

    audio = {"uri": request.audio_uri}
    config = {
        "enable_word_time_offsets": request.enable_word_time_offsets,
        "enable_speaker_diarization": request.enable_speaker_diarization,
        "language_code": request.language_code,
        "model": "video" if request.enable_speaker_diarization else "default",
    }

    operation = client.long_running_recognize(config, audio)
    print("Waiting for operation to complete...")
    return operation.operation.name
