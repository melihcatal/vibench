import argparse
import json
import os
import sys
from typing import Any

from openai import OpenAI


def _normalize_word_timestamps(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for word in words:
        normalized.append(
            {
                "word": word.get("word"),
                "start": word.get("start"),
                "end": word.get("end"),
                "confidence": word.get("confidence"),
            }
        )
    return normalized


def _normalize_segment_timestamps(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for segment in segments:
        normalized.append(
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "text": segment.get("text"),
            }
        )
    return normalized


def get_timestamps(transcription_result: Any, granularity: str = "word") -> list[dict[str, Any]]:
    if hasattr(transcription_result, "model_dump"):
        data = transcription_result.model_dump()
    elif isinstance(transcription_result, dict):
        data = transcription_result
    else:
        data = transcription_result.__dict__

    segments = data.get("segments") or []
    words: list[dict[str, Any]] = []
    for segment in segments:
        segment_words = segment.get("words") or []
        if segment_words:
            words.extend(segment_words)

    if granularity == "segment":
        return _normalize_segment_timestamps(segments)
    if granularity == "word":
        return _normalize_word_timestamps(words)
    raise ValueError("granularity must be 'word' or 'segment'")


def _load_transcription_result(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Return word or segment timestamps from an OpenAI transcription result.")
    parser.add_argument("transcription_result", help="Path to a JSON transcription result or audio file")
    parser.add_argument("--granularity", choices=("word", "segment"), default="word")
    args = parser.parse_args()

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        if args.transcription_result.lower().endswith(".json"):
            result = _load_transcription_result(args.transcription_result)
        else:
            with open(args.transcription_result, "rb") as audio_file:
                result = client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=[args.granularity],
                )
        timestamps = get_timestamps(result, args.granularity)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(timestamps, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
