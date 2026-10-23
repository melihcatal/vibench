import os
import json
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import EmbeddingResult


def embed_document_text(
    text: str,
    model_id: str = "amazon.titan-embed-text-v1",
    region: Optional[str] = None,
) -> EmbeddingResult:
    client = DocumentClient(region_name=region)
    bedrock_client = client.get_bedrock_client()

    request_body = {"inputText": text}

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())

    embedding = response_body.get("embedding", [])

    return EmbeddingResult(text=text, embedding=embedding, model_id=model_id)


def embed_multiple_texts(
    texts: List[str],
    model_id: str = "amazon.titan-embed-text-v1",
    region: Optional[str] = None,
) -> List[EmbeddingResult]:
    client = DocumentClient(region_name=region)
    bedrock_client = client.get_bedrock_client()

    results = []
    for text in texts:
        result = embed_document_text(text, model_id, region)
        results.append(result)

    return results


def embed_document_sections(
    sections: Dict[str, str],
    model_id: str = "amazon.titan-embed-text-v1",
    region: Optional[str] = None,
) -> Dict[str, EmbeddingResult]:
    results = {}
    for section_name, text in sections.items():
        if text:
            result = embed_document_text(text, model_id, region)
            results[section_name] = result

    return results


def embed_with_titan_multimodal(
    text: str, region: Optional[str] = None
) -> EmbeddingResult:
    return embed_document_text(
        text=text, model_id="amazon.titan-embed-text-v2:0", region=region
    )


def create_semantic_index(
    texts: List[str], region: Optional[str] = None
) -> Dict[str, Any]:
    embeddings = embed_multiple_texts(texts, region=region)

    index = {"documents": [], "embeddings": [], "metadata": []}

    for i, embedding_result in enumerate(embeddings):
        index["documents"].append(embedding_result.text)
        index["embeddings"].append(embedding_result.embedding)
        index["metadata"].append(
            {
                "model_id": embedding_result.model_id,
                "text_length": len(embedding_result.text),
            }
        )

    return index


def find_similar_documents(
    query: str,
    document_embeddings: List[EmbeddingResult],
    top_k: int = 5,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_embedding_result = embed_document_text(query, region=region)
    query_embedding = query_embedding_result.embedding

    similarities = []
    for i, doc_embedding in enumerate(document_embeddings):
        similarity = cosine_similarity(query_embedding, doc_embedding.embedding)
        similarities.append(
            {
                "index": i,
                "text": doc_embedding.text,
                "similarity": similarity,
                "model_id": doc_embedding.model_id,
            }
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_k]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def embed_for_retrieval(text: str, region: Optional[str] = None) -> List[float]:
    result = embed_document_text(text, region=region)
    return result.embedding
