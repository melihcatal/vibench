import argparse
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def load_segments(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("segments", "utterances", "transcript_segments"):
            value = data.get(key)
            if isinstance(value, list):
                return value
        raise ValueError("Input JSON must contain a segments-like list")
    if isinstance(data, list):
        return data
    raise ValueError("Unsupported transcript format")


def segment_text(segment: dict) -> str:
    if "text" in segment and isinstance(segment["text"], str):
        return segment["text"].strip()
    parts = []
    speaker = segment.get("speaker")
    if speaker is not None:
        parts.append(f"Speaker {speaker}")
    for key in ("start", "end"):
        if key in segment:
            parts.append(f"{key}={segment[key]}")
    text = segment.get("content") or segment.get("transcript") or ""
    if isinstance(text, str):
        text = text.strip()
    if text:
        parts.append(text)
    return " | ".join(parts).strip()


def embed_texts(texts: list[str], api_key: str, model: str = OPENAI_EMBEDDING_MODEL) -> list[list[float]]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers=headers,
        json={"model": model, "input": texts},
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()
    return [item["embedding"] for item in payload["data"]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Embed transcript segments for semantic retrieval using OpenAI embeddings.")
    parser.add_argument("transcript_file", help="Path to a transcript JSON file")
    parser.add_argument("--output", help="Optional output JSON file path")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Missing OPENAI_API_KEY environment variable", file=sys.stderr)
        return 1

    transcript_path = Path(args.transcript_file)
    if not transcript_path.is_file():
        print(f"Transcript file not found: {transcript_path}", file=sys.stderr)
        return 1

    segments = load_segments(transcript_path)
    texts = [segment_text(segment) for segment in segments]
    indexed = [(idx, text) for idx, text in enumerate(texts) if text]
    if not indexed:
        print("No embeddable transcript segments found", file=sys.stderr)
        return 1

    embeddings = embed_texts([text for _, text in indexed], api_key)
    results = []
    for (idx, text), embedding in zip(indexed, embeddings):
        segment = segments[idx]
        results.append({"index": idx, "segment": segment, "text": text, "embedding": embedding})

    output = json.dumps(results, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
