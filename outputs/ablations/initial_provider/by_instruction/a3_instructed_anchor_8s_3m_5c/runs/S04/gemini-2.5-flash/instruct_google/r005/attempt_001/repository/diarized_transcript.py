from speech_models import TranscriptionRequest, TranscriptionResult
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job

def get_diarized_transcript(audio_uri: str, language_code: str = "en-US") -> TranscriptionResult:
    request = TranscriptionRequest(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_speaker_diarization=True,
        enable_word_time_offsets=True # Diarization often goes with word offsets
    )
    operation_name = submit_transcription_job(request)
    result = poll_transcription_job(operation_name)
    return result
