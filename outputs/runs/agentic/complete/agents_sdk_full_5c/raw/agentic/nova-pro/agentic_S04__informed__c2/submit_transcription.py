import os
from assemblyai import TranscriptApiClient

client = TranscriptApiClient(api_key=os.getenv('ASSEMBLYAI_API_KEY'))

def submit_transcription(audio_file_path):
    transcript = client.transcripts.submit(audio_file_path)
    return transcript.id