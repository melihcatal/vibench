import time
import assemblyai as aai
from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription(
    transcript_id: str, timeout_seconds: int = 300
) -> TranscriptionResult:
    """Poll a transcription job and return the transcript."""
    client = get_speech_client()

    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        transcript = client.transcript.get(transcript_id)

        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResult(
                transcript_id=transcript_id,
                text=transcript.text,
                status="completed",
                words=[word.text for word in transcript.words]
                if transcript.words
                else [],
                segments=[
                    {"text": segment.text, "start": segment.start, "end": segment.end}
                    for segment in transcript.utterances or []
                ],
            )
        elif transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        time.sleep(2)

    raise TimeoutError(f"Transcription timed out after {timeout_seconds} seconds")
