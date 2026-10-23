import os
from assemblyai import Transcript, AAIClient

client = AAIClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))


def poll_transcription(transcript_id):
    transcript = client.get_transcript_by_id(transcript_id)
    return transcript.text
