"""
Translate queries before multilingual embedding search.

Provider: OpenAI Chat Completions API (GPT-4o mini for translation)
Provider SDK: openai
Provider Model: gpt-4o-mini / text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from openai import OpenAI

from embeddings_client import EmbeddingsClient
from embeddings_models import cosine_similarity, SearchResult


def translate_query(
    query: str,
    target_language: str = "English",
    source_language: str = "auto",
) -> str:
    """Translate a query to the target language using OpenAI GPT-4o mini.

    Args:
        query: The query text to translate.
        target_language: Target language name (default: English).
        source_language: Source language name (default: auto-detect).

    Returns:
        Translated query string in the target language.
    """
    client = OpenAI()
    system_prompt = (
        f"You are a translator. Translate the user's text from {source_language} "
        f"to {target_language}. Return only the translated text with no explanations."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=256,
    )
    translated = response.choices[0].message.content.strip()
    return translated


def multilingual_query_translate_and_search(
    query: str,
    documents: list[str],
    target_language: str = "English",
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
    top_k: int = 5,
) -> list[SearchResult]:
    """Translate a query and embed it alongside documents for multilingual semantic search.

    Uses GPT-4o mini to translate the query to the target language,
    then uses text-embedding-3-small to embed both query and documents.

    Args:
        query: Query text (may be in any language).
        documents: List of document strings to search.
        target_language: Language to translate the query into (default: English).
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Embedding output dimensions.
        top_k: Number of top results.

    Returns:
        Ranked list of SearchResult objects.
    """
    # Step 1: Translate query using GPT-4o mini via api.openai.com
    translated_query = translate_query(query, target_language=target_language)

    # Step 2: Embed the translated query and all documents using text-embedding-3-small
    client = EmbeddingsClient(model=model, dimensions=dimensions)
    query_embedding = client.embed(text=translated_query, dimensions=dimensions)
    doc_embeddings = client.embed_many(texts=documents, dimensions=dimensions)

    # Step 3: Score and rank
    scored: list[SearchResult] = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scored.append(SearchResult(document=documents[i], score=score, index=i))

    scored.sort(key=lambda r: r.score, reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    query_es = "¿Cómo funciona la inteligencia artificial?"
    docs = [
        "Artificial intelligence uses neural networks and deep learning.",
        "Machine learning algorithms improve with more training data.",
        "The weather forecast predicts rain tomorrow.",
        "Natural language processing enables computers to understand text.",
    ]
    results = multilingual_query_translate_and_search(query_es, docs, target_language="English", top_k=3)
    for r in results:
        print(f"[{r.score:.4f}] {r.document}")
