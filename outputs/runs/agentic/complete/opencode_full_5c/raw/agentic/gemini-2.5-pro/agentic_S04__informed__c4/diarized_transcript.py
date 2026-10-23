from typing import List
from speech_client import client
from speech_models import DiarizedSegment
from assemblyai import TranscriptionConfig, Transcript, TranscriptStatus
import time


def request_diarized_transcript(audio_path: str) -> List[DiarizedSegment]:
    """
    Requests a diarized transcript for a given audio file.
    """
    config = TranscriptionConfig(speaker_labels=True)
    transcript: Transcript = client.transcripts.create(audio_path, config=config)

    while True:
        result = client.transcripts.get(transcript.id)
        if result.status == TranscriptStatus.completed:
            if result.utterances is None:
                return []
            return [
                {"speaker": utterance.speaker, "text": utterance.text}
                for utterance in result.utterances
            ]
        elif result.status == TranscriptStatus.error:
            raise Exception(f"Transcription failed: {result.error}")
        time.sleep(5)
