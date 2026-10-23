from embeddings_client import get_gemini_client, get_embedding_model
from embeddings_models import EmbeddingBatchRequest, EmbeddingResponse
from typing import List


def embed_for_search(
    query_text: str, document_texts: List[str]
) -> (EmbeddingResponse, List[EmbeddingResponse]):
    client = get_gemini_client()
    model = get_embedding_model(client)

    query_embedding_result = model.embed_content(
        content=query_text, task_type="RETRIEVAL_QUERY"
    )
    query_embedding = EmbeddingResponse(embedding=query_embedding_result["embedding"])

    document_embeddings_result = model.embed_content(
        content=document_texts, task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [
        EmbeddingResponse(embedding=item["embedding"])
        for item in document_embeddings_result["embeddings"]
    ]

    return query_embedding, document_embeddings
