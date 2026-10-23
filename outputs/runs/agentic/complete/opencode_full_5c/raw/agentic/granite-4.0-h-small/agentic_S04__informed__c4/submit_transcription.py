import os
import json
from speech_client import SpeechClient


# Same-scenario: submit an audio file for batch transcription
def submit_transcription(audio_path):
    client = SpeechClient()
    # Build request payload using helper
    payload = client.create_batch_transcription_request(audio_path)
    # Submit via provider-specific SDK (Watson STT example)
    response = client.stt.submit_batch(payload)
    return response["job_id"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: submit_transcription.py <audio_file.wav>")
        sys.exit(1)
    job_id = submit_transcription(sys.argv[1])
    print(f"Transcription job submitted, ID: {job_id}")
