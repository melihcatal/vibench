import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: str = os.environ.get("OPENAI_API_KEY", "")
    model: str = OPENAI_EMBEDDING_MODEL
    endpoint: str = OPENAI_EMBEDDINGS_URL


def _require_api_key(api_key: str) -> str:
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def _normalize_text(section: Any) -> str:
    if section is None:
        return ""
    if isinstance(section, str):
        return section.strip()
    if isinstance(section, dict):
        for key in ("text", "content", "section_text", "body", "value"):
            value = section.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        parts: List[str] = []
        for value in section.values():
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())
        return "\n".join(parts).strip()
    return str(section).strip()


def _prepare_sections(sections: Any) -> List[Dict[str, Any]]:
    if isinstance(sections, str):
        parsed = json.loads(sections)
        sections = parsed
    if not isinstance(sections, Sequence) or isinstance(sections, (bytes, bytearray)):
        raise ValueError("sections must be a sequence of document sections")

    prepared: List[Dict[str, Any]] = []
    for index, section in enumerate(sections):
        text = _normalize_text(section)
        if not text:
            continue
        if isinstance(section, dict):
            item = dict(section)
        else:
            item = {"text": text}
        item.setdefault("section_id", item.get("id", index))
        item["text"] = text
        prepared.append(item)
    return prepared


def _embed_texts(texts: Sequence[str], config: Optional[EmbeddingConfig] = None) -> List[List[float]]:
    cfg = config or EmbeddingConfig()
    api_key = _require_api_key(cfg.api_key)
    response = requests.post(
        cfg.endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": cfg.model, "input": list(texts)},
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", [])
    embeddings: List[List[float]] = []
    for item in data:
        embedding = item.get("embedding")
        if embedding is not None:
            embeddings.append(embedding)
    if len(embeddings) != len(texts):
        raise RuntimeError("embedding response did not return one vector per input text")
    return embeddings


def embed_document_sections(sections: Any, config: Optional[EmbeddingConfig] = None) -> List[Dict[str, Any]]:
    prepared = _prepare_sections(sections)
    if not prepared:
        return []
    texts = [item["text"] for item in prepared]
    embeddings = _embed_texts(texts, config=config)
    results: List[Dict[str, Any]] = []
    for item, embedding in zip(prepared, embeddings):
        result = dict(item)
        result["embedding"] = embedding
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sections_file")
    args = parser.parse_args()

    with open(args.sections_file, "r", encoding="utf-8") as handle:
        sections = json.load(handle)

    sys.stdout.write(json.dumps(embed_document_sections(sections), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
