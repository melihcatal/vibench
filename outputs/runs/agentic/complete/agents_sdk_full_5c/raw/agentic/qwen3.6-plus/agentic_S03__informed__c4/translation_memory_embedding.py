"""
Embed translated segments for translation-memory search.

Provider: OpenAI / Azure OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY

Uses OpenAI's text-embedding-3-small or text-embedding-3-large models
to create vector embeddings of translated text segments. These embeddings
enable semantic similarity search across a translation memory, allowing
retrieval of previously translated segments that are semantically similar
to new source text.

Model: text-embedding-3-small (1536 dims) or text-embedding-3-large (3072 dims)
"""

import os
from typing import Optional

import openai

# Concrete OpenAI model identifiers
EMBEDDING_MODEL_SMALL = "text-embedding-3-small"
EMBEDDING_MODEL_LARGE = "text-embedding-3-large"


def get_openai_client() -> openai.OpenAI:
    """Create an OpenAI client using the API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Set it with your OpenAI API key."
        )
    return openai.OpenAI(api_key=api_key)


def embed_text_segment(
    text: str,
    *,
    model: str = EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
    client: Optional[openai.OpenAI] = None,
) -> list[float]:
    """
    Create an embedding vector for a single text segment.

    Args:
        text: The text to embed.
        model: OpenAI embedding model ID.
            Defaults to 'text-embedding-3-small' (1536 dimensions).
            Use 'text-embedding-3-large' for 3072 dimensions.
        dimensions: Optional output dimensionality reduction.
            For text-embedding-3-small: max 1536
            For text-embedding-3-large: max 3072
        client: Optional pre-created OpenAI client.

    Returns:
        List of floats representing the embedding vector.

    Raises:
        openai.OpenAIError: If the API request fails.
    """
    if not text or not text.strip():
        return []

    if client is None:
        client = get_openai_client()

    kwargs: dict = {
        "input": text,
        "model": model,
    }

    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    return response.data[0].embedding


def embed_translation_memory(
    segments: list[dict],
    *,
    model: str = EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
    client: Optional[openai.OpenAI] = None,
) -> list[dict]:
    """
    Embed a set of translation memory entries.

    Each entry contains source text, translated text, source language,
    and target language. Embeddings are created for both source and
    translated text to enable bidirectional search.

    Args:
        segments: List of dicts with keys:
            - 'source_text': original text
            - 'translated_text': translation
            - 'source_lang': source language code
            - 'target_lang': target language code
            - 'metadata': optional dict with additional info
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.
        client: Optional pre-created OpenAI client.

    Returns:
        List of dicts with original data plus 'source_embedding' and
        'translated_embedding' vectors.
    """
    if client is None:
        client = get_openai_client()

    results = []
    for segment in segments:
        source_text = segment.get("source_text", "")
        translated_text = segment.get("translated_text", "")

        source_embedding = embed_text_segment(
            text=source_text,
            model=model,
            dimensions=dimensions,
            client=client,
        )

        translated_embedding = embed_text_segment(
            text=translated_text,
            model=model,
            dimensions=dimensions,
            client=client,
        )

        entry = {
            **segment,
            "source_embedding": source_embedding,
            "translated_embedding": translated_embedding,
            "model": model,
            "dimensions": dimensions or len(source_embedding),
        }
        results.append(entry)

    return results


def search_translation_memory(
    query: str,
    memory_entries: list[dict],
    *,
    embedding_field: str = "source_embedding",
    top_k: int = 5,
) -> list[tuple[float, dict]]:
    """
    Search translation memory by semantic similarity.

    Computes cosine similarity between the query embedding and
    stored segment embeddings, returning the most similar matches.

    Args:
        query: The query text to search for.
        memory_entries: List of embedded translation memory entries.
        embedding_field: Which embedding field to search against.
            'source_embedding' to find by source text similarity.
            'translated_embedding' to find by translated text similarity.
        top_k: Number of results to return.

    Returns:
        List of (similarity_score, entry) tuples sorted by similarity.
    """
    if not query or not memory_entries:
        return []

    query_embedding = embed_text_segment(text=query)

    def cosine_similarity(a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    scored_entries = []
    for entry in memory_entries:
        stored_embedding = entry.get(embedding_field, [])
        if stored_embedding:
            similarity = cosine_similarity(query_embedding, stored_embedding)
            scored_entries.append((similarity, entry))

    scored_entries.sort(key=lambda x: x[0], reverse=True)
    return scored_entries[:top_k]


def embed_segments_batch(
    texts: list[str],
    *,
    model: str = EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
    client: Optional[openai.OpenAI] = None,
) -> list[list[float]]:
    """
    Embed multiple text segments in a single API call.

    OpenAI's embeddings API accepts an array of inputs, making batch
    embedding more efficient than individual calls.

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.
        client: Optional pre-created OpenAI client.

    Returns:
        List of embedding vectors, one per input text.
    """
    if not texts:
        return []

    if client is None:
        client = get_openai_client()

    # OpenAI API limits batch size; process in chunks of 2048
    batch_size = 2048
    all_embeddings: list[list[float]] = []

    for i in range(0, len(texts), batch_size):
        chunk = texts[i : i + batch_size]
        kwargs: dict = {
            "input": chunk,
            "model": model,
        }
        if dimensions is not None:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)

        for item in response.data:
            all_embeddings.append(item.embedding)

    return all_embeddings


if __name__ == "__main__":
    embedding = embed_text_segment(
        text="Hello, how are you today?",
        model=EMBEDDING_MODEL_SMALL,
    )
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
