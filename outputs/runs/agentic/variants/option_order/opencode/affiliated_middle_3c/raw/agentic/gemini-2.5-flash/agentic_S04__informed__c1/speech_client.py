import os
import time
from typing import Optional

import assemblyai as aai

from speech_models import TranscriptionResult, TranscriptSegment, WordTimestamp


def get_aai_client():
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return aai.Client()


def submit_aai_transcription(
    audio_url: str, diarization: bool = False, word_timestamps: bool = False
) -> str:
    config = aai.TranscriptionConfig(
        speaker_labels=diarization,
        word_timestamps=word_timestamps,
    )
    transcriber = get_aai_client()
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript.id


def poll_aai_transcription(job_id: str) -> TranscriptionResult:
    transcriber = get_aai_client()
    transcript = transcriber.get_transcript(job_id)

    while (
        transcript.status != aai.TranscriptStatus.completed
        and transcript.status != aai.TranscriptStatus.error
    ):
        time.sleep(5)  # Wait for 5 seconds before polling again
        transcript = transcriber.get_transcript(job_id)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    segments = None
    if transcript.paragraphs:
        segments = [
            TranscriptSegment(
                id=str(idx), start=p.start, end=p.end, text=p.text, speaker=p.speaker
            )
            for idx, p in enumerate(transcript.paragraphs)
        ]
    elif transcript.utterances:
        segments = [
            TranscriptSegment(
                id=str(idx), start=u.start, end=u.end, text=u.text, speaker=u.speaker
            )
            for idx, u in enumerate(transcript.utterances)
        ]

    words = None
    if transcript.words:
        words = [
            WordTimestamp(word=w.text, start=w.start, end=w.end, speaker=w.speaker)
            for w in transcript.words
        ]

    return TranscriptionResult(
        id=transcript.id,
        status=transcript.status.value,
        text=transcript.text,
        segments=segments,
        words=words,
    )


def get_aai_transcript(job_id: str) -> TranscriptionResult:
    transcriber = get_aai_client()
    transcript = transcriber.get_transcript(job_id)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    segments = None
    if transcript.paragraphs:
        segments = [
            TranscriptSegment(
                id=str(idx), start=p.start, end=p.end, text=p.text, speaker=p.speaker
            )
            for idx, p in enumerate(transcript.paragraphs)
        ]
    elif transcript.utterances:
        segments = [
            TranscriptSegment(
                id=str(idx), start=u.start, end=u.end, text=u.text, speaker=u.speaker
            )
            for idx, u in enumerate(transcript.utterances)
        ]

    words = None
    if transcript.words:
        words = [
            WordTimestamp(word=w.text, start=w.start, end=w.end, speaker=w.speaker)
            for w in transcript.words
        ]

    return TranscriptionResult(
        id=transcript.id,
        status=transcript.status.value,
        text=transcript.text,
        segments=segments,
        words=words,
    )
