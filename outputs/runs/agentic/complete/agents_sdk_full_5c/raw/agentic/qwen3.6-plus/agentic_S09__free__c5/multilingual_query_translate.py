"""
Translate queries before multilingual embedding search.

Provider: OpenAI Chat Completions API (https://api.openai.com)
Model: gpt-4o-mini
"""

from typing import List, Optional, Dict, Any

from openai import OpenAI

from embeddings_client import get_openai_client, load_embeddings_config


TRANSLATION_PROMPT_TEMPLATE = """\
Translate the following query from {source_language} to {target_language}.
Return only the translated query text, with no additional explanation.

Original query: {query}
"""


class TranslationResult:
    """
    Result of a query translation.

    Attributes:
        original_query: Original query text
        translated_query: Translated query text
        source_language: Source language code
        target_language: Target language code
        confidence: Estimated translation confidence (0.0 to 1.0)
    """

    def __init__(
        self,
        original_query: str,
        translated_query: str,
        source_language: str = "auto",
        target_language: str = "en",
        confidence: float = 1.0,
    ):
        self.original_query = original_query
        self.translated_query = translated_query
        self.source_language = source_language
        self.target_language = target_language
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_query": self.original_query,
            "translated_query": self.translated_query,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
        }


def translate_query(
    query: str,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> TranslationResult:
    """
    Translate a search query to a target language using OpenAI's GPT model.

    Uses the gpt-4o-mini model via OpenAI's Chat Completions API to translate
    queries before performing multilingual embedding search.

    Args:
        query: Original query text
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Source language code (default: 'auto')
        model: OpenAI chat model (default: gpt-4o-mini)
        api_key: OpenAI API key

    Returns:
        TranslationResult with translated query

    Raises:
        ValueError: If query is empty
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    client = get_openai_client(api_key=api_key)

    prompt = TRANSLATION_PROMPT_TEMPLATE.format(
        source_language=source_language,
        target_language=target_language,
        query=query,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate queries accurately from any language to {target_language}.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=256,
    )

    translated_text = response.choices[0].message.content.strip()

    return TranslationResult(
        original_query=query,
        translated_query=translated_text,
        source_language=source_language,
        target_language=target_language,
    )


def translate_queries_batch(
    queries: List[str],
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> List[TranslationResult]:
    """
    Translate multiple queries for multilingual embedding search.

    Args:
        queries: List of query texts to translate
        target_language: Target language code
        source_language: Source language code
        model: OpenAI chat model (default: gpt-4o-mini)
        api_key: OpenAI API key

    Returns:
        List of TranslationResult objects
    """
    results = []
    for query in queries:
        result = translate_query(
            query=query,
            target_language=target_language,
            source_language=source_language,
            model=model,
            api_key=api_key,
        )
        results.append(result)
    return results


def prepare_multilingual_search(
    query: str,
    documents: List[str],
    query_language: str = "auto",
    document_language: str = "en",
    embedding_model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Prepare a query and documents for multilingual semantic search.

    Translates the query to match the document language, then returns
    the translated query ready for embedding with OpenAI's text-embedding-3-small.

    Args:
        query: Search query (may be in any language)
        documents: List of documents (in document_language)
        query_language: Query source language
        document_language: Document language
        embedding_model: OpenAI embedding model for subsequent embedding
        api_key: OpenAI API key

    Returns:
        Dict with translated_query, documents, and embedding config
    """
    translation = translate_query(
        query=query,
        target_language=document_language,
        source_language=query_language,
        model="gpt-4o-mini",
        api_key=api_key,
    )

    config = load_embeddings_config()
    target_model = embedding_model or config["model"]

    return {
        "translated_query": translation.translated_query,
        "original_query": query,
        "documents": documents,
        "document_language": document_language,
        "embedding_model": target_model,
    }


if __name__ == "__main__":
    import json

    sample_query = "¿Cómo funciona el aprendizaje automático?"
    result = translate_query(sample_query, target_language="en")
    print(json.dumps(result.to_dict(), indent=2))
