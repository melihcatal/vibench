import time
import assemblyai as aai
from typing import Dict, Any
from speech_client import get_transcriber
from speech_models import TranscriptResponse


def poll_transcription(
    job_id: str, poll_interval: int = 10, timeout_seconds: int = 3600
) -> Dict[str, Any]:
    transcriber = get_transcriber()
    transcript = transcriber.get_transcript(job_id)
    start_time = time.time()
    while transcript.status == aai.TranscriptStatus.PROCESSING and (
        time.time() - start_time < timeout_seconds
    ):
        time.sleep(poll_interval)
        transcript = transcriber.get_transcript(job_id)
    if transcript.status == aai.TranscriptStatus.COMPLETED:
        words = [
            {
                "start": word.start,
                "end": word.end,
                "text": word.text,
                "confidence": getattr(word, "confidence", 0.0),
            }
            for word in transcript.words
        ]
        utterances = None
        if hasattr(transcript, "utterances") and transcript.utterances:
            utterances = [
                {
                    "speaker": utterance.speaker,
                    "start": utterance.start,
                    "end": utterance.end,
                    "text": utterance.text,
                }
                for utterance in transcript.utterances
            ]
        return {
            "job_id": str(transcript.id),
            "text": getattr(transcript, "text", ""),
            "words": words,
            "utterances": utterances,
        }
    elif transcript.status == aai.TranscriptStatus.ERROR:
        raise ValueError(
            f"Transcription error: {getattr(transcript, 'error', 'Unknown')}"
        )
    else:
        raise TimeoutError("Transcription timed out")
