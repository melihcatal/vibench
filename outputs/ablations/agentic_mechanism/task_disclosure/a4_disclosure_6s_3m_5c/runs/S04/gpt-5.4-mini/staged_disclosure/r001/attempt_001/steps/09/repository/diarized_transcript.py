import argparse
import json
import os
import sys
from pathlib import Path

import requests


ASSEMBLYAI_UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"


def upload_audio(path: Path, api_key: str) -> str:
    headers = {"authorization": api_key}
    with path.open("rb") as f:
        response = requests.post(ASSEMBLYAI_UPLOAD_URL, headers=headers, data=f, timeout=120)
    response.raise_for_status()
    return response.json()["upload_url"]


def create_diarized_transcript(upload_url: str, api_key: str) -> dict:
    payload = {"audio_url": upload_url, "speaker_labels": True}
    response = requests.post(
        ASSEMBLYAI_TRANSCRIPT_URL,
        headers={"authorization": api_key, "content-type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Request speaker diarization for a recorded meeting using AssemblyAI.")
    parser.add_argument("audio_file", help="Path to the audio or video file")
    args = parser.parse_args()

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("ASSEMBLYAI_API_KEY is required", file=sys.stderr)
        return 1

    path = Path(args.audio_file)
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    upload_url = upload_audio(path, api_key)
    transcript = create_diarized_transcript(upload_url, api_key)
    print(json.dumps(transcript, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
