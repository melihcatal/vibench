from speech_client import get_speech_client
from speech_models import TranscriptionConfig
from google.cloud.speech_v1p1beta1 import (
    RecognitionConfig,
    RecognitionAudio,
    LongRunningRecognizeRequest,
)


def submit_transcription_job(config: TranscriptionConfig) -> str:
    """Submits an audio file for batch transcription and returns the operation ID."""
    client = get_speech_client()

    audio = RecognitionAudio(uri=config.audio_uri)

    speech_config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming common audio encoding. Adjust if needed.
        sample_rate_hertz=16000,  # Assuming common sample rate. Adjust if needed.
        language_code=config.language_code,
        enable_automatic_punctuation=True,
    )

    # Only add diarization config if requested
    if config.enable_speaker_diarization:
        speech_config.diarization_config.enable_speaker_diarization = True
        speech_config.diarization_config.min_speaker_count = config.min_speaker_count
        speech_config.diarization_config.max_speaker_count = config.max_speaker_count

    # Only enable word time offsets if requested
    if config.enable_word_time_offsets:
        speech_config.enable_word_time_offsets = True

    request = LongRunningRecognizeRequest(config=speech_config, audio=audio)

    operation = client.long_running_recognize(request=request)
    print(f"Transcription operation submitted: {operation.operation.name}")
    return operation.operation.name
