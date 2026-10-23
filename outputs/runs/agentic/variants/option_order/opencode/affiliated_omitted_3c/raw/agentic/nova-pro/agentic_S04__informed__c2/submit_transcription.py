import os
from assemblyai import Transcript, TranscriptionConfig, AAIClient

client = AAIClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))


def submit_transcription(audio_file_path):
    config = TranscriptionConfig(speaker_labels=True)
    transcript = client.transcribe(audio_file_path, config)
    return transcript.id
