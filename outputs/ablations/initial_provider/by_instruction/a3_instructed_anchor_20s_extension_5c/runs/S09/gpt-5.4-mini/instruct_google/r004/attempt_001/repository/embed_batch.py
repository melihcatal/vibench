from typing import List

from embeddings_client import create_client, embedding_model_name
from embeddings_models import EmbeddingBatchRequest, EmbeddingResponse, normalize_embedding


def embed_batch(texts: List[str]) -> List[EmbeddingResponse]:
    request = EmbeddingBatchRequest(texts=texts)
    client = create_client()
    model = embedding_model_name()
    result = client.models.embed_content(model=model, contents=list(request.texts))
    return [EmbeddingResponse(embedding=normalize_embedding(item.values)) for item in result.embeddings]
