import os
import time
from typing import List, Dict
from assemblyai import Client
from speech_client import poll_transcript
from speech_models import get_diarize_config


def diarized_transcript(audio_file: str) -> List[Dict]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = Client(api_key=api_key)
    config = get_diarize_config()
    upload_url = client.upload(audio_file)
    transcript_input = client.transcripts.create(upload_url, config)
    transcript = poll_transcript(client, transcript_input.id)
    return [
        {
            "speaker": utterance.speaker,
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end,
            "confidence": utterance.confidence,
        }
        for utterance in transcript.utterances
    ]
