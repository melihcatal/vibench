from collections import Counter

from embeddings_models import normalize_vector
import google.generativeai as genai


def embedding_job_summary(vectors: list[list[float]]) -> dict[str, object]:
    counts = Counter(len(v) for v in vectors)
    summary_vector = normalize_vector([float(sum(values)) for values in zip(*vectors)]) if vectors else []
    return {"provider": "google", "vector_lengths": dict(counts), "summary_vector": summary_vector}
