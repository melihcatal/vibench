import assemblyai as aai
from assemblyai import TranscriptStatus
import time
from speech_client import get_client
from speech_models import TranscriptSegment, Word
from typing import List


def get_timestamped_transcript(
    job_id: str, poll_interval: int = 10, timeout: int = 3600
) -> List[TranscriptSegment]:
    client = get_client()
    start_time = time.time()
    while time.time() - start_time < timeout:
        transcript = client.transcripts.get(job_id)
        if transcript.status == TranscriptStatus.completed:
            return _extract_segments(transcript)
        elif transcript.status == TranscriptStatus.error:
            raise ValueError(
                f"Transcription error: {getattr(transcript, 'error', 'Unknown')}"
            )
        time.sleep(poll_interval)
    raise TimeoutError(f"Polling timed out after {timeout} seconds")


def _extract_segments(t: aai.Transcript) -> List[TranscriptSegment]:
    segments = []
    if t.utterances:
        for utterance in t.utterances:
            words = [
                Word(start=w.start, end=w.end, text=w.text, confidence=w.confidence)
                for w in utterance.words
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
        if t.words:
            words = [
                Word(start=w.start, end=w.end, text=w.text, confidence=w.confidence)
                for w in t.words
            ]
            segments.append(
                TranscriptSegment(
                    start=0, end=t.words[-1].end, text=t.text, words=words
                )
            )
    return segments
