import assemblyai as aai
import time
from speech_client import get_api_key

def timestamped_transcript(job_id: str):
    aai.settings.api_key = get_api_key()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript(job_id)
    while transcript.status == aai.TranscriptStatus.processing:
        time.sleep(10)
        transcript = transcriber.get_transcript(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    return [
        {
            "start": word.start / 1000.0,
            "end": word.end / 1000.0,
            "word": word.word,
            "confidence": word.confidence
        }
        for word in transcript.words
    ]
