# [SAME-SCENARIO] submit_transcription.py
# Submits an audio file for batch transcription using AssemblyAI Transcripts API
import os
import requests
from speech_client import get_auth_header

API_URL = "https://api.assemblyai.com/v2/transcription"
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def submit_transcription(audio_path: str) -> dict:
    """Submit an audio file for asynchronous batch transcription.

    Args:
        audio_path: Path to the audio file.
    Returns:
        JSON response from AssemblyAI containing the transcription ID.
    """
    headers = {"authorization": API_KEY} if API_KEY else get_auth_header()
    with open(audio_path, "rb") as audio_file:
        response = requests.post(API_URL, files={"audio": audio_file}, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python submit_transcription.py <path-to-audio>")
        sys.exit(1)
    result = submit_transcription(sys.argv[1])
    print("Transcription submitted, ID:", result.get("id"))
