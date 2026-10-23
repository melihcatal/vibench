"""
[LATER-STEP] crypto_audit_embedding.py - Embed crypto audit notes for semantic search.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embeddings(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embeddings for a list of text strings using OpenAI Embeddings API.

    Provider: OpenAI Embeddings API
    SDK: openai
    Auth: OPENAI_API_KEY
    Model: text-embedding-3-small
    """
    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not openai_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY env var or pass --api-key."
        )

    client = OpenAI(api_key=openai_api_key)

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embeddings = []
    for item in response.data:
        embeddings.append(item.embedding)

    logger.info(
        "Generated %d embeddings using OpenAI model %s",
        len(embeddings),
        model,
    )
    return embeddings


def embed_audit_notes(
    audit_notes: List[Dict[str, str]],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Embed crypto audit notes for semantic search.

    Each note should have at least a 'text' field. Additional metadata is preserved.

    Provider: OpenAI Embeddings API (openai SDK, text-embedding-3-small model)
    """
    texts = [note.get("text", "") for note in audit_notes]
    embeddings = generate_embeddings(
        texts=texts,
        model=model,
        api_key=api_key,
        dimensions=dimensions,
    )

    enriched_notes = []
    for note, embedding in zip(audit_notes, embeddings):
        enriched_note = {
            **note,
            "embedding": embedding,
            "note_id": note.get(
                "note_id", hashlib.sha256(note["text"].encode()).hexdigest()[:16]
            ),
            "timestamp": note.get("timestamp", datetime.utcnow().isoformat()),
            "model": model,
        }
        enriched_notes.append(enriched_note)

    return enriched_notes


def embed_crypto_audit_log(
    audit_entries: List[str],
    key_id: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Embed a list of crypto audit log entries for semantic search.

    Provider: OpenAI Embeddings API
    """
    audit_notes = [
        {
            "text": entry,
            "key_id": key_id,
            "entry_index": idx,
        }
        for idx, entry in enumerate(audit_entries)
    ]

    return embed_audit_notes(
        audit_notes=audit_notes,
        model=model,
        api_key=api_key,
    )


def search_similar_notes(
    query: str,
    embedded_notes: List[Dict[str, Any]],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search for notes most similar to a query using cosine similarity.

    Provider: OpenAI Embeddings API (for query embedding)
    """
    query_embedding = generate_embeddings(
        texts=[query],
        model=model,
        api_key=api_key,
    )[0]

    scored_notes = []
    for note in embedded_notes:
        embedding = note.get("embedding")
        if not embedding:
            continue

        score = _cosine_similarity(query_embedding, embedding)
        scored_notes.append(
            {
                **note,
                "similarity_score": score,
            }
        )

    scored_notes.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_notes[:top_k]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Embed crypto audit notes for semantic search"
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    embed_parser = subparsers.add_parser("embed", help="Embed audit notes")
    embed_parser.add_argument(
        "--notes-file",
        required=True,
        help="Path to JSON file with audit notes",
    )
    embed_parser.add_argument(
        "--output-file",
        required=True,
        help="Path to write embedded notes",
    )
    embed_parser.add_argument("--api-key", help="OpenAI API key")
    embed_parser.add_argument("--model", default=OPENAI_EMBEDDING_MODEL)

    search_parser = subparsers.add_parser("search", help="Search embedded notes")
    search_parser.add_argument(
        "--embedded-file",
        required=True,
        help="Path to JSON file with embedded notes",
    )
    search_parser.add_argument(
        "--query",
        required=True,
        help="Search query text",
    )
    search_parser.add_argument("--top-k", type=int, default=5)
    search_parser.add_argument("--api-key", help="OpenAI API key")
    search_parser.add_argument("--model", default=OPENAI_EMBEDDING_MODEL)

    args = parser.parse_args()

    if args.action == "embed":
        with open(args.notes_file, "r") as f:
            audit_notes = json.load(f)

        embedded = embed_audit_notes(
            audit_notes=audit_notes,
            model=args.model,
            api_key=args.api_key,
        )

        with open(args.output_file, "w") as f:
            json.dump(embedded, f, indent=2, default=str)
        print(f"Embedded {len(embedded)} notes to {args.output_file}")

    elif args.action == "search":
        with open(args.embedded_file, "r") as f:
            embedded_notes = json.load(f)

        results = search_similar_notes(
            query=args.query,
            embedded_notes=embedded_notes,
            model=args.model,
            api_key=args.api_key,
            top_k=args.top_k,
        )

        for i, result in enumerate(results, 1):
            print(
                f"{i}. [{result['similarity_score']:.4f}] {result.get('text', '')[:100]}"
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
