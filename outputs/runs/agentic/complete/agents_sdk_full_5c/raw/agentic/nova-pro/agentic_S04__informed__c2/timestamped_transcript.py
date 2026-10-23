import os
from assemblyai import TranscriptApiClient

client = TranscriptApiClient(api_key=os.getenv('ASSEMBLYAI_API_KEY'))

def timestamped_transcript(transcript_id):
    transcript = client.transcripts.get(transcript_id)
    return transcript.words if transcript.status == 'completed' else None