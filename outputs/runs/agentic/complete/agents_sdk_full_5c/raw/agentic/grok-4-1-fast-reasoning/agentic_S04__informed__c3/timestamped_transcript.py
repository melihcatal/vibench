import assemblyai as aai
from speech_client import get_speech_client
from speech_models import get_diarized_words

def timestamped_transcript(job_id: str) -> list:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != aai.TranscriptStatus.completed:
        raise ValueError(f'Transcript not ready: {transcript.status}')
    return get_diarized_words(transcript)