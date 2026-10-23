import os
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


def submit_transcription(audio_url: str, *, language_code: Optional[str] = None, speaker_labels: bool = False, punctuate: bool = True) -> Dict[str, Any]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    payload: Dict[str, Any] = {"audio_url": audio_url, "punctuate": punctuate}
    if language_code:
        payload["language_code"] = language_code
    if speaker_labels:
        payload["speaker_labels"] = True

    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/transcript",
        headers={"authorization": api_key, "content-type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("audio_url")
    parser.add_argument("--language-code")
    parser.add_argument("--speaker-labels", action="store_true")
    parser.add_argument("--no-punctuate", action="store_true")
    args = parser.parse_args()

    result = submit_transcription(
        args.audio_url,
        language_code=args.language_code,
        speaker_labels=args.speaker_labels,
        punctuate=not args.no_punctuate,
    )
    print(json.dumps(result, indent=2))
