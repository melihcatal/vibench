import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests


OPENAI_BATCH_ENDPOINT = "https://api.openai.com/v1/batches"
OPENAI_FILES_ENDPOINT = "https://api.openai.com/v1/files"
OPENAI_TRANSCRIPTION_ENDPOINT = "/v1/audio/transcriptions"


def upload_file(path: Path, api_key: str) -> str:
    with path.open("rb") as f:
        response = requests.post(
            OPENAI_FILES_ENDPOINT,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (path.name, f, "application/octet-stream")},
            data={"purpose": "batch"},
            timeout=120,
        )
    response.raise_for_status()
    return response.json()["id"]


def create_batch(input_file_id: str, api_key: str) -> dict:
    payload = {
        "input_file_id": input_file_id,
        "endpoint": OPENAI_TRANSCRIPTION_ENDPOINT,
        "completion_window": "24h",
    }
    response = requests.post(
        OPENAI_BATCH_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit an audio file for OpenAI batch transcription.")
    parser.add_argument("audio_file", help="Path to the audio file to submit")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is required", file=sys.stderr)
        return 1

    path = Path(args.audio_file)
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    input_file_id = upload_file(path, api_key)
    batch = create_batch(input_file_id, api_key)
    print(json.dumps(batch, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
