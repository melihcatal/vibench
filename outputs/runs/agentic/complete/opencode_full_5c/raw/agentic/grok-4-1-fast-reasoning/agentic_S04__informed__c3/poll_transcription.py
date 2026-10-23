import assemblyai as aai
from speech_client import get_api_key


def poll_transcription(job_id: str) -> dict:
    api_key = get_api_key()
    client = aai.Client(api_key=api_key)
    transcript = client.transcripts.get(job_id)
    while transcript.status != aai.TranscriptStatus.completed:
        transcript = client.transcripts.get(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f"Transcription error: {transcript.error}")
    return dict(transcript.json_response)
