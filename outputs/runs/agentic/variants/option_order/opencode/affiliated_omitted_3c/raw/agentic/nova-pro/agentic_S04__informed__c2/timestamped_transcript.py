import os
from assemblyai import Transcript, TranscriptionConfig, AAIClient

client = AAIClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))


def timestamped_transcript(audio_file_path):
    config = TranscriptionConfig(word_timestamps=True)
    transcript = client.transcribe(audio_file_path, config)
    return transcript.words
