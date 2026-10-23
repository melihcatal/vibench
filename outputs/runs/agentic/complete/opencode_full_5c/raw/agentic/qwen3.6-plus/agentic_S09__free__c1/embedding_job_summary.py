from typing import List
from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import EmbeddingJobSummary


def embedding_job_summary(texts: List[str]) -> EmbeddingJobSummary:
    client = get_openai_client()
    model = get_embedding_model()

    summary = EmbeddingJobSummary(
        total_texts=len(texts),
        model=model,
    )

    try:
        api_response = client.embeddings.create(
            model=model,
            input=texts,
            encoding_format="float",
        )

        if api_response.usage:
            summary.total_tokens = api_response.usage.total_tokens

        if api_response.data:
            first_embedding = api_response.data[0].embedding
            summary.embedding_dimension = len(first_embedding)

            norms = []
            for item in api_response.data:
                magnitude = sum(x * x for x in item.embedding) ** 0.5
                norms.append(magnitude)
            summary.average_norm = sum(norms) / len(norms) if norms else 0.0

    except Exception as e:
        summary.errors.append(str(e))

    return summary


if __name__ == "__main__":
    import json

    texts = [
        "OpenAI provides embedding models",
        "Semantic search uses vector similarity",
        "Text embeddings capture meaning",
    ]
    summary = embedding_job_summary(texts)
    print(
        json.dumps(
            {
                "total_texts": summary.total_texts,
                "total_tokens": summary.total_tokens,
                "embedding_dimension": summary.embedding_dimension,
                "model": summary.model,
                "average_norm": round(summary.average_norm, 4),
                "errors": summary.errors,
            },
            indent=2,
        )
    )
