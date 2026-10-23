import os
from typing import Any, Dict, List, Mapping, Optional, Sequence

import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


def _require_api_key(api_key: Optional[str] = None) -> str:
    token = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not token:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return token


def _segment_text(segment: Mapping[str, Any]) -> str:
    text = segment.get("text")
    return "" if text is None else str(text)


def _normalize_segments(segments: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for segment in segments:
        normalized.append(dict(segment))
    return normalized


def translate_transcript(
    transcript: Mapping[str, Any],
    target_language_code: str,
    *,
    api_key: Optional[str] = None,
    timeout_seconds: int = 60,
) -> Dict[str, Any]:
    token = _require_api_key(api_key)
    transcript_id = str(transcript.get("id") or transcript.get("transcript_id") or "")
    if not transcript_id:
        raise ValueError("transcript id is required")

    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}/translate",
        headers={"authorization": token, "content-type": "application/json"},
        json={"target_language_code": target_language_code},
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    payload = response.json()
    translated_segments = payload.get("segments") or payload.get("utterances") or []
    return {
        "transcript_id": transcript_id,
        "target_language_code": target_language_code,
        "status": payload.get("status"),
        "translated_text": payload.get("translated_text") or payload.get("text") or payload.get("translation"),
        "segments": _normalize_segments(translated_segments) if isinstance(translated_segments, list) else [],
        "response": payload,
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_id")
    parser.add_argument("target_language_code")
    parser.add_argument("--api-key")
    args = parser.parse_args()

    result = translate_transcript({"id": args.transcript_id}, args.target_language_code, api_key=args.api_key)
    print(json.dumps(result, indent=2))
