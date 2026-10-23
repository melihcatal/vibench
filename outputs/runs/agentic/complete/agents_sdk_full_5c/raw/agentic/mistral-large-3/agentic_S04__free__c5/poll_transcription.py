from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TranscriptionResponse

def poll_transcription(job_name: str) -> TranscriptionResponse:
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    
    job = client.get_recognizer_job(name=job_name)
    if job.state == cloud_speech.RecognizerJob.State.SUCCEEDED:
        transcript = ""
        for result in job.results:
            transcript += result.alternatives[0].transcript + " "
        
        return TranscriptionResponse(
            job_name=job.name,
            transcript=transcript.strip(),
            is_complete=True,
            metadata={"language_code": job.config.language_codes[0]}
        )
    elif job.state == cloud_speech.RecognizerJob.State.FAILED:
        raise RuntimeError(f"Transcription job failed: {job.name}")
    else:
        return TranscriptionResponse(
            job_name=job.name,
            transcript="",
            is_complete=False,
            metadata={}
        )