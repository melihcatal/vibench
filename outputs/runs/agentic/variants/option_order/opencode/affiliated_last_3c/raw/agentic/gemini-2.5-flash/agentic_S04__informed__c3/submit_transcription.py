from speech_client import speech_client
from speech_models import TranscriptionRequest


def submit_transcription(request: TranscriptionRequest):
    audio = {"uri": request.audio_uri}
    config = {
        "enable_word_time_offsets": request.enable_word_time_offsets,
        "enable_speaker_diarization": request.enable_speaker_diarization,
        "language_code": request.language_code,
    }
    operation = speech_client.speech_client.long_running_recognize(
        config=config, audio=audio
    )
    print("Waiting for operation to complete...")
    return operation.operation.name
