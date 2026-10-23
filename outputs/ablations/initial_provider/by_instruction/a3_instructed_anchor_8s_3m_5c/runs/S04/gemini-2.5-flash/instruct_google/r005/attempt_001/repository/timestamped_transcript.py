from speech_models import TranscriptionRequest, TranscriptionResult
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job

def get_timestamped_transcript(audio_uri: str, language_code: str = "en-US") -> TranscriptionResult:
    request = TranscriptionRequest(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_word_time_offsets=True,
        enable_speaker_diarization=False # Not strictly needed for timestamps, but can be enabled if desired
    )
    operation_name = submit_transcription_job(request)
    result = poll_transcription_job(operation_name)
    return result
