from speech_models import TranscriptionConfig, TranscriptionResult
from submit_transcription import submit_transcription
from poll_transcription import poll_transcription

def timestamped_transcript(audio_uri: str, language_code: str = "en-US") -> TranscriptionResult:
    """Returns word or segment timestamps from a transcription result.

    Args:
        audio_uri: The URI of the audio file to transcribe.
        language_code: The language code of the audio.

    Returns:
        A TranscriptionResult object with word-level timestamps.
    """
    config = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_word_time_offsets=True
    )
    job = submit_transcription(config)
    result = poll_transcription(job)
    return result
