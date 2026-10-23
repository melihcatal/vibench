from collections import Counter

from embeddings_client import get_openai_client
from embeddings_models import normalize_embedding_response

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def summarize_embedding_job(job_texts: list[str]) -> dict[str, object]:
    client = get_openai_client()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=job_texts)
    vectors = normalize_embedding_response(response)
    lengths = [len(v) for v in vectors]
    return {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "count": len(vectors),
        "dimension_histogram": dict(Counter(lengths)),
        "average_dimension": (sum(lengths) / len(lengths)) if lengths else 0,
    }
