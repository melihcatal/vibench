from collections import Counter

from embeddings_client import get_openai_embeddings_client
from embeddings_models import normalize_embedding_response


OPENAI_MODEL = "text-embedding-3-large"


def embedding_job_summary(job_records):
    client = get_openai_embeddings_client()
    texts = [record["text"] for record in job_records]
    response = client.embeddings.create(model=OPENAI_MODEL, input=texts)
    normalized = normalize_embedding_response(response)
    dimensions = len(normalized.embeddings[0]) if normalized.embeddings else 0
    metadata = Counter(record.get("source", "unknown") for record in job_records)
    return {
        "model": OPENAI_MODEL,
        "count": len(normalized.embeddings),
        "dimensions": dimensions,
        "sources": dict(metadata),
    }
