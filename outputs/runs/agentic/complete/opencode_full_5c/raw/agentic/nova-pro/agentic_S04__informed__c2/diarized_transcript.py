import os
from assemblyai import Transcript, AssemblyAI

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

client = AssemblyAI(api_key=ASSEMBLYAI_API_KEY)


def request_diarization(audio_file_path):
    transcript = client.transcripts.submit(audio_file_path, speaker_labels=True)
    return transcript.id
