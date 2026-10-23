import os
import assemblyai as aai
from speech_client import get_assemblyai_client


def timestamped_transcript(job_id):
    """Return word or segment timestamps from a transcription result."""
    client = get_assemblyai_client()

    transcript = client.transcript.get(job_id)

    if transcript.status != aai.TranscriptStatus.completed:
        return {
            "job_id": job_id,
            "status": transcript.status,
            "error": transcript.error
            if transcript.status == aai.TranscriptStatus.error
            else "Transcription not completed",
            "provider": "AssemblyAI",
        }

    word_timestamps = []
    if transcript.words:
        for word in transcript.words:
            word_timestamps.append(
                {
                    "text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.confidence,
                }
            )

    segment_timestamps = []
    if transcript.utterances:
        for utterance in transcript.utterances:
            segment_timestamps.append(
                {
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                    "speaker": utterance.speaker,
                    "confidence": utterance.confidence,
                }
            )

    return {
        "job_id": job_id,
        "status": "completed",
        "word_timestamps": word_timestamps,
        "segment_timestamps": segment_timestamps,
        "full_text": transcript.text,
        "provider": "AssemblyAI",
    }
