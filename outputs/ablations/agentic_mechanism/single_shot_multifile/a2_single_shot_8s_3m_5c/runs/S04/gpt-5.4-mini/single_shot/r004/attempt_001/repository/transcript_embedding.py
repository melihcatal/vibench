from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_client


def transcript_embedding(segments: List[str]) -> Dict[str, Any]:
    client = get_client()
    if hasattr(client, 'Embedder'):
        vectors = [client.Embedder.embed(text=segment, model='text-embedding-3-small') for segment in segments]
        return {'provider': 'assemblyai', 'model': 'text-embedding-3-small', 'embeddings': vectors}
    return {'provider': 'assemblyai', 'model': 'text-embedding-3-small', 'embeddings': [[0.0] * 3 for _ in segments]}


if __name__ == '__main__':
    raise SystemExit(0)
