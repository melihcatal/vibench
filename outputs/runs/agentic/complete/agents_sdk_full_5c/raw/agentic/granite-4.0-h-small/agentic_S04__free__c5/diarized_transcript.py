import os
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobRequest

def diarized_transcript(audio_file_path: str, job_id: str) -> str:
    """Request a transcription with speaker diarization.
    
    Args:
        audio_file_path: Path to the audio file stored in the configured bucket.
        job_id: Identifier for the job (used for polling later).
    
    Returns:
        The transcript text with speaker labels (depends on provider format).
    """
    client = BatchSpeechClient()
    # Build request with diarization flag enabled via helper
    request = TranscriptionJobRequest(
        audio_uri=f'gs://{os.getenv(''BATCH_SPEECH_BUCKET'')}/{audio_file_path}',
        enable_diarization=True,
        enable_timestamps=False,
        model=os.getenv('BATCH_SPEECH_MODEL_ID', 'en-US-Transcribe')
    )
    # Submit as a regular job (provider will honor diarization flag)
    client.create_transcription_job(request=request, location=os.getenv('BATCH_SPEECH_LOCATION', 'us-central1'), project=os.getenv('BATCH_SPEECH_PROJECT_ID'))
    # For brevity we delegate polling and result extraction to poll_transcription
    return poll_transcription(job_id)
