import assemblyai as aai
from assemblyai import TranscriptStatus
import time
from speech_client import get_client
from speech_models import Transcript, TranscriptSegment, Word
from typing import List


def poll_transcription(
    job_id: str, poll_interval: int = 10, timeout: int = 3600
) -> Transcript:
    client = get_client()
    start_time = time.time()
    while time.time() - start_time < timeout:
        transcript = client.transcripts.get(job_id)
        if transcript.status == TranscriptStatus.completed:
            return _parse_transcript(transcript)
        elif transcript.status == TranscriptStatus.error:
            raise ValueError(
                f"Transcription error: {getattr(transcript, 'error', 'Unknown error')}"
            )
        time.sleep(poll_interval)
    raise TimeoutError(f"Polling timed out after {timeout} seconds")


def _parse_transcript(t: aai.Transcript) -> Transcript:
    segments: List[TranscriptSegment] = []
    if t.utterances:
        for utterance in t.utterances:
            words = [
                Word(
                    start=word.start,
                    end=word.end,
                    text=word.text,
                    confidence=word.confidence,
                )
                for word in utterance.words
            ]
            segments.append(
                TranscriptSegment(
                    start=utterance.start,
                    end=utterance.end,
                    text=utterance.text,
                    speaker=utterance.speaker,
                    words=words,
                )
            )
    else:
        words = [
            Word(
                start=word.start,
                end=word.end,
                text=word.text,
                confidence=word.confidence,
            )
            for word in t.words
        ]
        segments.append(
            TranscriptSegment(
                start=0,
                end=max((word.end for word in words), default=0),
                text=t.text,
                words=words,
            )
        )
    return Transcript(id=t.id, text=t.text, segments=segments)
