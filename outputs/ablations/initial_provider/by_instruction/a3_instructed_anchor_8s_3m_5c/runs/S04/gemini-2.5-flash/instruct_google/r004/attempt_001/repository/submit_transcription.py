from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionConfig, TranscriptionJob

def submit_transcription(config: TranscriptionConfig) -> TranscriptionJob:
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        config: Configuration for the transcription job.

    Returns:
        A TranscriptionJob object representing the submitted job.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=config.audio_uri)
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16 for example, can be customized
        sample_rate_hertz=16000, # Assuming 16000 for example, can be customized
        language_code=config.language_code,
        enable_speaker_diarization=config.enable_speaker_diarization,
        enable_word_time_offsets=config.enable_word_time_offsets,
    )

    operation = client.long_running_recognize(config=recognition_config, audio=audio)

    # The operation name can be used to poll the status of the transcription job.
    return TranscriptionJob(name=operation.operation.name, status="SUBMITTED")
