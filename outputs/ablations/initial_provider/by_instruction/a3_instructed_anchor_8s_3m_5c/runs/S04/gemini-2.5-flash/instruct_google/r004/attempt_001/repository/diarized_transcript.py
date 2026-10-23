from speech_models import TranscriptionConfig, TranscriptionResult
from submit_transcription import submit_transcription
from poll_transcription import poll_transcription

def diarized_transcript(audio_uri: str, language_code: str = "en-US") -> TranscriptionResult:
    """Requests speaker diarization for a recorded meeting and returns the diarized transcript.

    Args:
        audio_uri: The URI of the audio file to transcribe.
        language_code: The language code of the audio.

    Returns:
        A TranscriptionResult object with speaker diarization information.
    """
    config = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_speaker_diarization=True,
        enable_word_time_offsets=True  # Word time offsets are usually needed for diarization
    )
    job = submit_transcription(config)
    result = poll_transcription(job)
    return result
