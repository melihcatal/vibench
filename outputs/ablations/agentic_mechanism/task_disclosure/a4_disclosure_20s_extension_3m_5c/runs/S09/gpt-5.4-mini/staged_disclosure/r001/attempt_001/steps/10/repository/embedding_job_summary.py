import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _provider_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def summarize_embedding_job(job: Dict[str, Any]) -> Dict[str, Any]:
    inputs: List[str] = job.get("inputs", [])
    if not isinstance(inputs, list):
        raise TypeError("job['inputs'] must be a list of strings")

    payload = {"model": OPENAI_EMBEDDING_MODEL, "input": inputs}
    response = requests.post(OPENAI_EMBEDDINGS_URL, json=payload, headers=_provider_headers(), timeout=60)
    response.raise_for_status()
    data = response.json()

    embeddings = data.get("data", [])
    dims = len(embeddings[0]["embedding"]) if embeddings else 0

    return {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "input_count": len(inputs),
        "embedding_count": len(embeddings),
        "embedding_dimensions": dims,
        "usage": data.get("usage", {}),
    }


def main(job: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if job is None:
        job = {"inputs": [os.getenv("EMBEDDING_SUMMARY_TEXT", "example text")]}
    return summarize_embedding_job(job)


if __name__ == "__main__":
    print(main())
