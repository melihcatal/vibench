import os
from assemblyai import Transcript, AssemblyAI

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

client = AssemblyAI(api_key=ASSEMBLYAI_API_KEY)


def submit_transcription(audio_file_path):
    transcript = client.transcripts.submit(audio_file_path)
    return transcript.id
