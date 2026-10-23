import os
from google.cloud import speech_v1
from google.oauth2 import service_account


def get_speech_client():
    """Get a configured Google Cloud Speech-to-Text client."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = speech_v1.SpeechClient(credentials=credentials)
    else:
        client = speech_v1.SpeechClient()

    return client


def get_default_config(
    language_code="en-US", enable_word_time_offsets=True, model="video"
):
    """Get default recognition configuration."""
    from google.cloud.speech_v1 import RecognitionConfig

    return RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
    )


def create_diarization_config(min_speaker_count=2, max_speaker_count=5):
    """Create speaker diarization configuration."""
    from google.cloud.speech_v1 import SpeakerDiarizationConfig

    return SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=min_speaker_count,
        max_speaker_count=max_speaker_count,
    )
