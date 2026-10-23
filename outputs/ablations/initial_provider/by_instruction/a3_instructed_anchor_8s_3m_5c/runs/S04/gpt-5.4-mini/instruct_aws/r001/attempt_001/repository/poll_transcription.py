from speech_client import get_transcribe_client


def poll_transcription(job_name: str):
    client = get_transcribe_client()
    return client.get_transcription_job(TranscriptionJobName=job_name)
