import os
import time
from typing import List, Dict
from assemblyai import Client
from speech_client import poll_transcript


def timestamped_transcript(job_id: str) -> List[Dict]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = Client(api_key=api_key)
    transcript = poll_transcript(client, job_id)
    return [
        {
            "text": word.text,
            "start": word.start,
            "end": word.end,
            "confidence": word.confidence,
        }
        for word in transcript.words
    ]
