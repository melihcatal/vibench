from speech_client import submit_aai_transcription


def submit_transcription_job(
    audio_url: str, enable_diarization: bool = False, enable_timestamping: bool = False
) -> str:
    """Submits an audio file for batch transcription using AssemblyAI."""
    job_id = submit_aai_transcription(
        audio_url, diarization=enable_diarization, word_timestamps=enable_timestamping
    )
    return job_id
