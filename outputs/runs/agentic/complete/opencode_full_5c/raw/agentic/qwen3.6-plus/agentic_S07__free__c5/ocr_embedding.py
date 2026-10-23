from typing import List, Optional, Dict, Any
import os
import openai
from document_models import EmbeddingRequest, EmbeddingResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_section(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> EmbeddingResponse:
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    params: Dict[str, Any] = {"input": text, "model": model}
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    embedding = response.data[0].embedding
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return EmbeddingResponse(
        embedding=embedding,
        model=model,
        usage=usage,
        raw_response={
            "object": response.object,
            "model": response.model,
            "usage": usage,
        },
    )


def embed_document_sections(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[EmbeddingResponse]:
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    params: Dict[str, Any] = {"input": texts, "model": model}
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    results = []
    for idx, data in enumerate(response.data):
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        results.append(
            EmbeddingResponse(
                embedding=data.embedding,
                model=model,
                usage=usage,
                raw_response={
                    "object": response.object,
                    "model": response.model,
                    "usage": usage,
                },
            )
        )
    return results


def embed_ocr_blocks_for_retrieval(
    ocr_text: str,
    block_texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, List[float]]:
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    all_texts = [ocr_text] + block_texts
    response = client.embeddings.create(
        input=all_texts,
        model=model,
    )
    embeddings_map = {}
    embeddings_map["document"] = response.data[0].embedding
    for idx, data in enumerate(response.data[1:], start=1):
        embeddings_map[f"block_{idx - 1}"] = data.embedding
    return embeddings_map


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
