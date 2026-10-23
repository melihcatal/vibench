import os
from assemblyai import TranscriptApiClient

client = TranscriptApiClient(api_key=os.getenv('ASSEMBLYAI_API_KEY'))

def poll_transcription(transcript_id):
    transcript = client.transcripts.get(transcript_id)
    return transcript.text