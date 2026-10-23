import os
import sys
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from security_models import AuditEmbedding


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_audit_notes(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> AuditEmbedding:
    client = get_openai_client()
    kwargs: Dict[str, Any] = {
        "model": model,
        "input": text,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    data = response.data[0]
    embedding = data.embedding
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return AuditEmbedding(
        text=text,
        embedding=embedding,
        model=model,
        usage=usage,
    )


def embed_multiple_audit_notes(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[AuditEmbedding]:
    client = get_openai_client()
    kwargs: Dict[str, Any] = {
        "model": model,
        "input": texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    results = []
    for item in response.data:
        results.append(
            AuditEmbedding(
                text=texts[item.index] if item.index < len(texts) else "",
                embedding=item.embedding,
                model=model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            )
        )
    return results


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def main():
    text = sys.stdin.read()
    if not text.strip():
        print("Error: No audit note text provided on stdin", file=sys.stderr)
        sys.exit(1)
    model = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    dimensions = None
    dim_env = os.environ.get("EMBEDDING_DIMENSIONS")
    if dim_env:
        dimensions = int(dim_env)
    result = embed_audit_notes(text, model, dimensions)
    output = {
        "text": result.text,
        "model": result.model,
        "embedding_dimension": len(result.embedding),
        "usage": result.usage,
        "embedding_preview": result.embedding[:10],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
