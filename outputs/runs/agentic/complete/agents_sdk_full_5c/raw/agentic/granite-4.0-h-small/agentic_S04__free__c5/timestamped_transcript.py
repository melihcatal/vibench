import os
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobRequest

def timestamped_transcript(audio_file_path: str, job_id: str) -> str:
    """Request a transcription that includes word/segment timestamps.
    
    Args:
        audio_file_path: Path to the audio file in the configured bucket.
        job_id: Identifier for the job (used for polling later).
    
    Returns:
        A JSON string representing an array of word objects, each with start and end times.
    """
    client = BatchSpeechClient()
    # Enable timestamps via request helper
    request = TranscriptionJobRequest(
        audio_uri=f'gs://{os.getenv(''BATCH_SPEECH_BUCKET'')}/{audio_file_path}',
        enable_timestamps=True,
        enable_diarization=False,
        model=os.getenv('BATCH_SPEECH_MODEL_ID', 'en-US-Transcribe')
    )
    client.create_transcription_job(request=request, location=os.getenv('BATCH_SPEECH_LOCATION', 'us-central1'), project=os.getenv('BATCH_SPEECH_PROJECT_ID'))
    # Poll until SUCCESS then extract timestamps (provider may embed them in the result)
    return poll_transcription(job_id)
