import os
import json
from speech_client import SpeechClient


# Same-scenario: request word/segment timestamps from transcription result
def timestamped_transcript(job_id):
    client = SpeechClient()
    # Ask provider for timestamped output (Watson STT example)
    response = client.stt.get_transcription_with_timestamps(job_id)
    return response["timestamps"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: timestamped_transcript.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    timestamps = timestamped_transcript(job_id)
    print(f"Timestamps for job {job_id}:", timestamps)
