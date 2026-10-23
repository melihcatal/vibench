import os
from typing import Dict

import assemblyai as aai


def tts_qa_transcript(audio_url: str) -> Dict[str, object]:
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
    transcript = aai.Transcriber().transcribe(audio_url)
    return {"text": transcript.text, "id": transcript.id, "status": transcript.status}
