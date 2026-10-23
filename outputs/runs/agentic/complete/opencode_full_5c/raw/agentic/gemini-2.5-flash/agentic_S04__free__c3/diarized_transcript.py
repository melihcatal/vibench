from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_result
from speech_models import TranscriptionConfig, TranscriptionResult


def get_diarized_transcript(
    audio_uri: str,
    language_code: str = "en-US",
    min_speakers: int = 1,
    max_speakers: int = 6,
) -> TranscriptionResult:
    """Requests speaker diarization for a recorded meeting and returns the diarized transcript."""
    config = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_speaker_diarization=True,
        min_speaker_count=min_speakers,
        max_speaker_count=max_speakers,
        enable_word_time_offsets=True,  # Word time offsets are useful for diarization
    )

    operation_id = submit_transcription_job(config)
    result = poll_transcription_result(operation_id)

    return result
