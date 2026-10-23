import os
from assemblyai import TranscriptApiClient

client = TranscriptApiClient(api_key=os.getenv('ASSEMBLYAI_API_KEY'))

def diarized_transcript(audio_file_path):
    transcript = client.transcripts.submit(audio_file_path, speaker_labels=True)
    return transcript.utterances