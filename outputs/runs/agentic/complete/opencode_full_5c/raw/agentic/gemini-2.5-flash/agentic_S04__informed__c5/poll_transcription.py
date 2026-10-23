import os
import time
from speech_client import SpeechClient
from speech_models import TranscriptionResult, Segment, Word


def poll_transcription(job_id: str) -> TranscriptionResult:
    client = SpeechClient()
    speech_config = client.get_speech_config()

    # In a real scenario, this would involve polling Azure's batch transcription API
    # to check the job status and retrieve the results once completed.
    # For this example, we'll simulate a completed job with some mock data.

    print(f"Polling job {job_id}...")
    time.sleep(5)  # Simulate polling delay

    if job_id.startswith("mock_job_"):
        # Simulate a successful transcription result
        mock_segments = [
            Segment(
                text="Hello world,",
                offset=0,
                duration=1000,
                words=[
                    Word(word="Hello", offset=0, duration=500),
                    Word(word="world,", offset=500, duration=500),
                ],
                speaker=1,
            ),
            Segment(
                text="this is a test.",
                offset=1500,
                duration=1500,
                words=[
                    Word(word="this", offset=1500, duration=300),
                    Word(word="is", offset=1800, duration=200),
                    Word(word="a", offset=2000, duration=100),
                    Word(word="test.", offset=2100, duration=900),
                ],
                speaker=2,
            ),
        ]
        return TranscriptionResult(
            job_id=job_id, status="Completed", segments=mock_segments
        )
    else:
        return TranscriptionResult(job_id=job_id, status="Failed", segments=[])
