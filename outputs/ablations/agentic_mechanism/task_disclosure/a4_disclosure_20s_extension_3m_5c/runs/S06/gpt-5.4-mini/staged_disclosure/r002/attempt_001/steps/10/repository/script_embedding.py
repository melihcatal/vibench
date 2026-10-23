import hashlib
import json
import os
from typing import Iterable, List, Optional

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_script(script: str) -> str:
    return " ".join(script.split()).strip()


def _chunk_text(text: str, max_chars: int = 8000) -> List[str]:
    text = _normalize_script(text)
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split_at = text.rfind(" ", start, end)
            if split_at > start + max_chars // 2:
                end = split_at
        chunks.append(text[start:end].strip())
        start = end
    return [chunk for chunk in chunks if chunk]


def _openai_headers() -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def embed_scripts(scripts: Iterable[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[dict]:
    payload_texts = []
    script_map = []
    for index, script in enumerate(scripts):
        for chunk_index, chunk in enumerate(_chunk_text(script)):
            payload_texts.append(chunk)
            script_map.append((index, chunk_index, chunk))

    if not payload_texts:
        return []

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers=_openai_headers(),
        json={"model": model, "input": payload_texts},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()["data"]

    results = []
    for item, (script_index, chunk_index, chunk_text) in zip(data, script_map):
        results.append(
            {
                "script_index": script_index,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text,
                "embedding": item["embedding"],
                "model": model,
                "provider": "openai",
                "fingerprint": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest(),
            }
        )
    return results


def embed_script(script: str, model: str = OPENAI_EMBEDDING_MODEL) -> dict:
    embeddings = embed_scripts([script], model=model)
    return embeddings[0] if embeddings else {}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Embed narration scripts for voice-asset search using OpenAI.")
    parser.add_argument("input", help="Path to a JSON file containing a list of scripts or an object with a scripts field")
    parser.add_argument("--output", default="-", help="Output path for embeddings JSON, or - for stdout")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    scripts = payload.get("scripts") if isinstance(payload, dict) else payload
    if not isinstance(scripts, list):
        raise ValueError("Input must be a list of scripts or an object with a scripts list")

    result = embed_scripts([str(script) for script in scripts])
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)


if __name__ == "__main__":
    main()
