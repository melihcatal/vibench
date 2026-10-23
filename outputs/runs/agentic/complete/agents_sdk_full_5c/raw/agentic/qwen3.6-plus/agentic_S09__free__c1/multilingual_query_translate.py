"""Translate queries before multilingual embedding search using OpenAI API."""

import os
from typing import List, Dict, Optional, Any
from openai import OpenAI

from embeddings_client import get_openai_client
from embed_for_search import embed_for_search


def translate_query(
    query: str,
    source_language: str,
    target_language: str = "en",
    model: str = "gpt-4o-mini",
) -> str:
    """Translate a query from source language to target language.

    Uses OpenAI's gpt-4o-mini model for translation before embedding.
    This enables cross-lingual semantic search by translating queries
    into the language of the document corpus.

    Args:
        query: The query text to translate.
        source_language: Source language code (e.g., 'es', 'fr', 'zh').
        target_language: Target language code (default 'en').
        model: OpenAI chat model for translation.

    Returns:
        Translated query string.
    """
    client = get_openai_client()

    system_prompt = (
        f"You are a professional translator. Translate the user's query from "
        f"{source_language} to {target_language}. "
        f"Return only the translated text with no explanations or additional text."
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


def translate_batch_queries(
    queries: List[str],
    source_language: str,
    target_language: str = "en",
    model: str = "gpt-4o-mini",
) -> List[str]:
    """Translate multiple queries in batch.

    Uses OpenAI's gpt-4o-mini model to translate queries for multilingual search.

    Args:
        queries: List of query strings to translate.
        source_language: Source language code.
        target_language: Target language code.
        model: OpenAI chat model for translation.

    Returns:
        List of translated query strings.
    """
    client = get_openai_client()

    system_prompt = (
        f"You are a professional translator. Translate each query from "
        f"{source_language} to {target_language}. "
        f"Return only the translations, one per line, with no additional text."
    )

    queries_text = "\n".join(f"Q{i+1}: {q}" for i, q in enumerate(queries))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": queries_text},
        ],
        temperature=0.0,
        max_tokens=2000,
    )

    translated_text = response.choices[0].message.content.strip()
    translated_lines = [line.strip() for line in translated_text.split("\n") if line.strip()]

    # Extract translations (remove "Q1: " prefixes if present)
    translations = []
    for line in translated_lines:
        cleaned = line
        if ":" in line and line.split(":")[0].strip().startswith("Q"):
            cleaned = line.split(":", 1)[1].strip()
        translations.append(cleaned)

    return translations[:len(queries)]


def multilingual_search(
    query: str,
    documents: List[str],
    source_language: str,
    document_language: str = "en",
    embedding_model: str = "text-embedding-3-small",
    translation_model: str = "gpt-4o-mini",
    top_k: int = 5,
) -> Dict[str, Any]:
    """Perform semantic search with automatic query translation.

    Translates a query from source_language to document_language using OpenAI's
    gpt-4o-mini, then searches documents using OpenAI's text-embedding-3-small.

    Args:
        query: Query in source language.
        documents: Document texts in document_language.
        source_language: Query's source language code.
        document_language: Documents' language code.
        embedding_model: OpenAI embedding model.
        translation_model: OpenAI translation model.
        top_k: Number of results to return.

    Returns:
        Dict with translated query, search results, and metadata.
    """
    # Translate query to document language
    translated_query = translate_query(
        query,
        source_language=source_language,
        target_language=document_language,
        model=translation_model,
    )

    # Perform semantic search with translated query
    search_results = embed_for_search(
        query=translated_query,
        documents=documents,
        model=embedding_model,
        top_k=top_k,
    )

    return {
        "original_query": query,
        "source_language": source_language,
        "translated_query": translated_query,
        "document_language": document_language,
        "results": search_results,
        "provider": "OpenAI",
        "embedding_model": embedding_model,
        "translation_model": translation_model,
        "api_endpoints": {
            "embeddings": "https://api.openai.com/v1/embeddings",
            "chat_completions": "https://api.openai.com/v1/chat/completions",
        },
    }


def detect_and_translate(
    query: str,
    documents: List[str],
    target_language: str = "en",
    embedding_model: str = "text-embedding-3-small",
    translation_model: str = "gpt-4o-mini",
    top_k: int = 5,
) -> Dict[str, Any]:
    """Auto-detect query language, translate if needed, then search.

    Uses OpenAI's gpt-4o-mini to detect language and translate if necessary,
    then uses text-embedding-3-small for semantic search.

    Args:
        query: Query text in any language.
        documents: English document texts.
        target_language: Language of the documents.
        embedding_model: OpenAI embedding model.
        translation_model: OpenAI translation model.
        top_k: Number of results to return.

    Returns:
        Search results with translation metadata.
    """
    client = get_openai_client()

    # Detect language
    detection_response = client.chat.completions.create(
        model=translation_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Detect the language of the user's text. "
                    "Return only the ISO 639-1 language code (e.g., 'en', 'es', 'fr', 'zh', 'ja')."
                ),
            },
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=10,
    )

    detected_language = detection_response.choices[0].message.content.strip().lower()

    if detected_language == target_language:
        translated_query = query
    else:
        translated_query = translate_query(
            query,
            source_language=detected_language,
            target_language=target_language,
            model=translation_model,
        )

    search_results = embed_for_search(
        query=translated_query,
        documents=documents,
        model=embedding_model,
        top_k=top_k,
    )

    return {
        "original_query": query,
        "detected_language": detected_language,
        "translated_query": translated_query,
        "results": search_results,
        "provider": "OpenAI",
        "models_used": {
            "translation": translation_model,
            "embedding": embedding_model,
        },
    }


if __name__ == "__main__":
    docs = [
        "Climate change is causing rising sea levels worldwide.",
        "Renewable energy adoption is accelerating globally.",
        "The stock market reached record highs this week.",
        "New artificial intelligence models are transforming healthcare.",
    ]

    # Spanish query about climate
    result = multilingual_search(
        query="¿Cuáles son los efectos del cambio climático?",
        documents=docs,
        source_language="es",
        document_language="en",
        top_k=2,
    )
    print(f"Original: {result['original_query']}")
    print(f"Translated: {result['translated_query']}")
    for r in result['results']:
        print(f"  Score: {r['score']:.4f} | {r['document'][:60]}...")
