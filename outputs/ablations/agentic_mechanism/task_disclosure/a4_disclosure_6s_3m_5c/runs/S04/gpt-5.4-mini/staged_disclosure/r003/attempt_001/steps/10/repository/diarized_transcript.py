import argparse
import json
import os
import sys

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def _headers() -> dict:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return {"authorization": api_key, "content-type": "application/json"}


def _upload_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        response = requests.post(
            f"{ASSEMBLYAI_API_BASE}/upload",
            headers={"authorization": os.environ["ASSEMBLYAI_API_KEY"]},
            data=f,
            timeout=120,
        )
    response.raise_for_status()
    return response.json()["upload_url"]


def _create_diarized_transcript(audio_url: str) -> str:
    payload = {"audio_url": audio_url, "speaker_labels": True}
    response = requests.post(f"{ASSEMBLYAI_API_BASE}/transcript", headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["id"]


def _get_transcript(transcript_id: str) -> dict:
    response = requests.get(f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}", headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def request_speaker_diarization(audio_path: str) -> dict:
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(audio_path)
    audio_url = _upload_audio(audio_path)
    transcript_id = _create_diarized_transcript(audio_url)
    return _get_transcript(transcript_id)


def main() -> int:
    parser = argparse.ArgumentParser(description="Request speaker diarization for a recorded meeting using AssemblyAI.")
    parser.add_argument("audio_file", help="Path to the recorded meeting audio file")
    args = parser.parse_args()

    try:
        result = request_speaker_diarization(args.audio_file)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
