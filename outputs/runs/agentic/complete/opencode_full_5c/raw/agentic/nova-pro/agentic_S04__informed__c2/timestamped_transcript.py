import os
from assemblyai import Transcript, AssemblyAI

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

client = AssemblyAI(api_key=ASSEMBLYAI_API_KEY)


def get_timestamps(transcript_id):
    transcript = client.transcripts.get(transcript_id)
    return transcript.utterances if transcript.status == "completed" else None
