import os
import json
import urllib.request
import urllib.error
from typing import Optional

from observability_models import LogEntry


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_messages(
    entries: list[LogEntry],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[dict]:
    results = []
    batch_size = 100
    texts = []
    for entry in entries:
        if entry.message:
            texts.append((entry.id, entry.message))
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        batch_texts = [t[1] for t in batch]
        embeddings_response = _call_openai_embeddings(
            texts=batch_texts, api_key=api_key, model=model
        )
        embedding_data = embeddings_response.get("data", [])
        for idx, emb in enumerate(embedding_data):
            if idx < len(batch):
                log_id = batch[idx][0]
                results.append(
                    {
                        "log_id": log_id,
                        "embedding": emb.get("embedding", []),
                        "model": model,
                        "provider": "openai",
                        "index": emb.get("index", idx),
                    }
                )
    return results


def _call_openai_embeddings(
    texts: list[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> dict:
    url = f"{OPENAI_API_BASE}/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or OPENAI_API_KEY}",
    }
    payload = {
        "input": texts,
        "model": model,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"OpenAI text-embedding-3-small API error {e.code}: {e.reason} - {error_body}"
        ) from e
