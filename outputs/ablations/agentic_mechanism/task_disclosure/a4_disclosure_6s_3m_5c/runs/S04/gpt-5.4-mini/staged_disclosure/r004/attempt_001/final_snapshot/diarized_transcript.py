import argparse
import os
import sys
import time
from pathlib import Path

import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


def submit_audio(audio_path: str, api_key: str) -> str:
    headers = {"authorization": api_key}
    with open(audio_path, "rb") as f:
        upload = requests.post(
            f"{ASSEMBLYAI_BASE_URL}/upload",
            headers=headers,
            data=f,
            timeout=120,
        )
    upload.raise_for_status()
    return upload.json()["upload_url"]


def create_transcript(upload_url: str, api_key: str) -> str:
    headers = {"authorization": api_key, "content-type": "application/json"}
    payload = {"audio_url": upload_url, "speaker_labels": True}
    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/transcript",
        headers=headers,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["id"]


def poll_transcript(transcript_id: str, api_key: str) -> dict:
    headers = {"authorization": api_key}
    while True:
        response = requests.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        if status == "completed":
            return data
        if status == "error":
            raise RuntimeError(data.get("error", "AssemblyAI transcription failed"))
        time.sleep(5)


def format_diarized_transcript(data: dict) -> str:
    utterances = data.get("utterances") or []
    if utterances:
        lines = []
        for item in utterances:
            speaker = item.get("speaker", "Unknown")
            text = item.get("text", "").strip()
            if text:
                lines.append(f"Speaker {speaker}: {text}")
        return "\n".join(lines)
    text = data.get("text", "")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Request speaker diarization for a recorded meeting using AssemblyAI.")
    parser.add_argument("audio_file", help="Path to the recorded meeting audio file")
    args = parser.parse_args()

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Missing ASSEMBLYAI_API_KEY environment variable", file=sys.stderr)
        return 1

    audio_path = Path(args.audio_file)
    if not audio_path.is_file():
        print(f"Audio file not found: {audio_path}", file=sys.stderr)
        return 1

    upload_url = submit_audio(str(audio_path), api_key)
    transcript_id = create_transcript(upload_url, api_key)
    transcript = poll_transcript(transcript_id, api_key)
    print(format_diarized_transcript(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
