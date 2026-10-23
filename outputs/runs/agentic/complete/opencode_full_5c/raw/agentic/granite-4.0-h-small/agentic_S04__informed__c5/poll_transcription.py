# [SAME-SCENARIO] poll_transcription.py
# Polls a submitted transcription job and returns the completed transcript using AssemblyAI Transcripts API
import os
import requests
import time
from speech_client import get_auth_header

API_URL = "https://api.assemblyai.com/v2/transcription/{}"
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def poll_transcription(transcription_id: str, poll_interval: float = 5.0) -> dict:
    """Poll the transcription status until complete and return the transcript.

    Args:
        transcription_id: ID returned from submit_transcription.
        poll_interval: Seconds to wait between status checks.
    Returns:
        JSON response from AssemblyAI containing the transcript text and words list.
    """
    headers = {"authorization": API_KEY} if API_KEY else get_auth_header()
    while True:
        resp = requests.get(API_URL.format(transcription_id), headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "completed":
            return data
        time.sleep(poll_interval)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python poll_transcription.py <transcription-id>")
        sys.exit(1)
    transcript = poll_transcription(sys.argv[1])
    print("Transcript:", transcript.get("text"))
