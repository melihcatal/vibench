import assemblyai as aai
import os
from speech_client import get_assemblyai_client
from typing import Dict, Any


def get_timestamped_transcript(transcript_id: str) -> Dict[str, Any]:
    """
    Returns word or segment timestamps from an AssemblyAI transcription result.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_assemblyai_client()

    transcript = client.transcripts.get(transcript_id)

    if transcript.status == aai.TranscriptStatus.completed:
        words_with_timestamps = [
            {"word": word.text, "start": word.start, "end": word.end}
            for word in transcript.words
        ]
        return {"transcript_text": transcript.text, "words": words_with_timestamps}
    else:
        return {
            "status": transcript.status,
            "message": "Transcription not completed yet.",
        }
