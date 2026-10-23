import assemblyai as aai
from speech_client import get_api_key
from speech_models import parse_timestamped_transcript


def timestamped_transcript(job_id: str) -> list[dict]:
    api_key = get_api_key()
    client = aai.Client(api_key=api_key)
    transcript = client.transcripts.get(job_id)
    while transcript.status != aai.TranscriptStatus.completed:
        transcript = client.transcripts.get(job_id)
    result = dict(transcript.json_response)
    return parse_timestamped_transcript(result)
