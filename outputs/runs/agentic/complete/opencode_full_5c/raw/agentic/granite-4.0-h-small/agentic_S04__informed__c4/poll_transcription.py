import os
import json
from speech_client import SpeechClient


# Same-scenario: poll a batch transcription job and return the transcript
def poll_transcription(job_id):
    client = SpeechClient()
    # Provider-specific polling (Watson STT example)
    result = client.stt.poll_batch(job_id)
    if result["status"] == "completed":
        return result["transcript"]
    else:
        raise RuntimeError(f"Job not completed yet: {result['status']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: poll_transcription.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    transcript = poll_transcription(job_id)
    print(f"Transcript for job {job_id}:", transcript)
