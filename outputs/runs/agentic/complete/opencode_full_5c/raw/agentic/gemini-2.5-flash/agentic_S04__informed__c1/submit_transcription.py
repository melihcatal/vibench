import os
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionConfig


def submit_transcription_job(config: TranscriptionConfig) -> str:
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        config: Configuration for the transcription job.

    Returns:
        The name of the long-running operation (job ID).
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=config.audio_uri)
    config_obj = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Example, adjust as needed
        sample_rate_hertz=config.sample_rate_hertz
        or 16000,  # Example, adjust as needed
        language_code=config.language_code,
        enable_word_time_offsets=config.enable_word_time_offsets,
        enable_speaker_diarization=config.enable_speaker_diarization,
        # diarization_config=speech.SpeakerDiarizationConfig(enable_speaker_diarization=True, min_speaker_count=2, max_speaker_count=4) if config.enable_speaker_diarization else None,
    )

    # For long audio files, use long_running_recognize
    operation = client.long_running_recognize(config=config_obj, audio=audio)

    # The operation.name can be used to poll for results later
    return operation.operation_id.split("/")[-1]
