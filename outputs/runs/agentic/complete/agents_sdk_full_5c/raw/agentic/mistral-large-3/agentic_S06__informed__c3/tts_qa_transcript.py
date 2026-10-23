import os
import assemblyai as aai
from typing import List


def transcribe_audio(file_paths: List[str]) -> List[str]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY must be set in environment variables.")

    aai.settings.api_key = api_key
    transcripts = []

    for file_path in file_paths:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        transcripts.append(transcript.text)

    return transcripts