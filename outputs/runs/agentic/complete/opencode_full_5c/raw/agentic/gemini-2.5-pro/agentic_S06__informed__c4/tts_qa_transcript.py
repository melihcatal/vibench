import os
import assemblyai as aai
from typing import Optional


def transcribe_qa_sample(audio_file_path: str) -> Optional[str]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return transcript.error
    else:
        return transcript.text
