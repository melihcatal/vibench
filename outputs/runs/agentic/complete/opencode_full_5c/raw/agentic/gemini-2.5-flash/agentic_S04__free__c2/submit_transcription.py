from speech_client import get_speech_client
from speech_models import TranscriptionRequest
from google.cloud import speech_v1p1beta1 as speech


def submit_transcription(request: TranscriptionRequest) -> str:
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16, user might need to adjust
        sample_rate_hertz=16000,  # Assuming 16000 Hz, user might need to adjust
        language_code=request.language_code,
        enable_automatic_punctuation=request.enable_automatic_punctuation,
        enable_speaker_diarization=request.enable_speaker_diarization,
        enable_word_time_offsets=request.enable_word_time_offsets,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name
