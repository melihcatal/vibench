"""
Translate queries before multilingual embedding search using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: gpt-4o-mini (translation), text-embedding-3-small (embeddings)
"""

from typing import List, Dict, Any, Optional, Tuple

from openai import OpenAI

from embeddings_client import get_openai_client, resolve_model, OPENAI_EMBEDDING_API_HOST
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    cosine_similarity,
    normalize_vector,
)


# Provider-specific translation model identifier
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_query(
    query: str,
    target_language: str = "en",
    api_key: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> str:
    """
    Translate a query to the target language using OpenAI Chat Completions API.

    Args:
        query: The query string to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        api_key: OpenAI API key.
        model: OpenAI model identifier for translation.

    Returns:
        Translated query string.
    """
    client = get_openai_client(api_key=api_key)

    system_prompt = (
        f"You are a professional translator. Translate the following text "
        f"to {target_language}. Return only the translated text, nothing else."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=500,
    )

    translated = response.choices[0].message.content.strip()
    return translated


def translate_and_embed_query(
    query: str,
    target_language: str = "en",
    embedding_model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a query to target language and embed it for search.

    Args:
        query: The query string to translate and embed.
        target_language: Target language code.
        embedding_model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions for embedding.
        api_key: OpenAI API key.

    Returns:
        Dictionary with original_query, translated_query, embedding, and models used.
    """
    translated = translate_query(query, target_language, api_key=api_key)

    resolved_model = resolve_model(embedding_model)

    client = get_openai_client(api_key=api_key)

    request = BatchEmbeddingRequest(
        texts=[translated],
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    return {
        "original_query": query,
        "translated_query": translated,
        "target_language": target_language,
        "embedding": batch_result.embeddings[0],
        "translation_model": OPENAI_TRANSLATION_MODEL,
        "embedding_model": resolved_model,
        "provider": "openai",
        "api_host": OPENAI_EMBEDDING_API_HOST,
    }


def multilingual_semantic_search(
    query: str,
    documents: List[str],
    query_language: Optional[str] = None,
    document_language: str = "en",
    embedding_model: Optional[str] = None,
    dimensions: Optional[int] = None,
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate query if needed and perform semantic search across documents.

    Args:
        query: The search query (may be in any language).
        documents: List of document strings (expected in document_language).
        query_language: Language of the query (if None, auto-translate to document_language).
        document_language: Language of the documents.
        embedding_model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        top_k: Number of top results.
        api_key: OpenAI API key.

    Returns:
        List of ranked search results with translated query info.
    """
    resolved_model = resolve_model(embedding_model)

    # Translate query to document language if needed
    if query_language and query_language != document_language:
        translated_query = translate_query(
            query, target_language=document_language, api_key=api_key
        )
    else:
        translated_query = query

    client = get_openai_client(api_key=api_key)

    # Embed translated query and all documents
    all_texts = [translated_query] + documents
    request = BatchEmbeddingRequest(
        texts=all_texts,
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    query_vec = normalize_vector(batch_result.embeddings[0])

    scored_results = []
    for i, doc_vec in enumerate(batch_result.embeddings[1:]):
        doc_vec_norm = normalize_vector(doc_vec)
        score = cosine_similarity(query_vec, doc_vec_norm)
        scored_results.append({
            "index": i,
            "document": documents[i],
            "similarity_score": score,
        })

    scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {
        "results": scored_results[:top_k],
        "original_query": query,
        "translated_query": translated_query,
        "query_language": query_language,
        "document_language": document_language,
        "translation_model": OPENAI_TRANSLATION_MODEL,
        "embedding_model": resolved_model,
    }


if __name__ == "__main__":
    sample_docs = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing enables computers to understand text.",
    ]

    results = multilingual_semantic_search(
        query="¿Qué es el aprendizaje automático?",
        documents=sample_docs,
        query_language="es",
        document_language="en",
        top_k=2,
    )

    print(f"Original query: {results['original_query']}")
    print(f"Translated query: {results['translated_query']}")
    for r in results["results"]:
        print(f"  Score: {r['similarity_score']:.4f} | {r['document']}")
