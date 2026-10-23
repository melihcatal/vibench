from speech_client import get_assemblyai_client
import assemblyai as aai
from typing import List, Dict

def get_timestamped_transcript(audio_url: str) -> List[Dict]:
    """
    Transcribes an audio file and returns word-level timestamps.
    This is a blocking call that waits for the transcript to complete.
    """
    aai_client = get_assemblyai_client()
    transcriber = aai_client.Transcriber()
    
    # Word timestamps are included by default
    transcript = transcriber.transcribe(audio_url)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if not transcript.words:
        return []

    return [
        {"word": word.text, "start": word.start, "end": word.end}
        for word in transcript.words
    ]
