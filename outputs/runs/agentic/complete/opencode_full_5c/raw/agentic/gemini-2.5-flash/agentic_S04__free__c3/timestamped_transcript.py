from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_result
from speech_models import TranscriptionConfig, TranscriptionResult


def get_timestamped_transcript(
    audio_uri: str, language_code: str = "en-US"
) -> TranscriptionResult:
    """Returns word or segment timestamps from a transcription result."""
    config = TranscriptionConfig(
        audio_uri=audio_uri, language_code=language_code, enable_word_time_offsets=True
    )

    operation_id = submit_transcription_job(config)
    result = poll_transcription_result(operation_id)

    return result
