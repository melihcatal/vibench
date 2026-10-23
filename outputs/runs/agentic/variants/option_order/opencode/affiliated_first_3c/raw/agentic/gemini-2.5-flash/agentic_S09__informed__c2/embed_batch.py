from embeddings_client import get_gemini_client, get_embedding_model
from embeddings_models import EmbeddingBatchRequest, EmbeddingResponse
from typing import List


def embed_batch(request: EmbeddingBatchRequest) -> List[EmbeddingResponse]:
    client = get_gemini_client()
    model = get_embedding_model(client)
    result = model.embed_content(content=request.texts, task_type="SEMANTIC_SIMILARITY")
    return [
        EmbeddingResponse(embedding=item["embedding"]) for item in result["embeddings"]
    ]
