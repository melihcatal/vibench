from statistics import mean

from embeddings_client import embed_inputs
from embeddings_models import vector_from_response_item


def embedding_job_summary(texts):
    response = embed_inputs(texts)
    vectors = [vector_from_response_item(item) for item in response.data]
    dimensions = [len(vector) for vector in vectors]
    return {"count": len(vectors), "avg_dimension": mean(dimensions) if dimensions else 0, "provider": "openai"}
