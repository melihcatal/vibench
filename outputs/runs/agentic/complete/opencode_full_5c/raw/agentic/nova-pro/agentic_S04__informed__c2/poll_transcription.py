import os
from assemblyai import Transcript, AssemblyAI

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

client = AssemblyAI(api_key=ASSEMBLYAI_API_KEY)


def poll_transcription(transcript_id):
    transcript = client.transcripts.get(transcript_id)
    return transcript.text if transcript.status == "completed" else None
