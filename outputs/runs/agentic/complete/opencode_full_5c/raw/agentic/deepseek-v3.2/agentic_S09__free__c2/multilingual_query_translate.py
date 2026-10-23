import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


def translate_query_for_search(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate queries before multilingual embedding search using OpenAI's translation capabilities.

    Args:
        query: The search query string to translate
        target_language: Target language code (default: "en" for English)
        source_language: Source language code (optional, auto-detected if not provided)

    Returns:
        Dict containing translation results
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Prepare translation prompt
    if source_language:
        system_prompt = f"You are a professional translator. Translate the following text from {source_language} to {target_language}. Provide only the translation."
    else:
        system_prompt = f"You are a professional translator. Detect the language of the following text and translate it to {target_language}. Provide only the translation."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        translated_text = response.choices[0].message.content.strip()

        # Get detected language if not provided
        if not source_language:
            # Use a separate call to detect language
            detection_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Detect the language of the following text. Respond with only the ISO 639-1 language code.",
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0.1,
                max_tokens=10,
            )
            detected_language = detection_response.choices[0].message.content.strip()
        else:
            detected_language = source_language

        result = {
            "original_query": query,
            "translated_query": translated_text,
            "source_language": detected_language,
            "target_language": target_language,
            "translation_success": True,
            "model_used": "gpt-4o-mini",
            "provider": "OpenAI",
        }

        return result

    except Exception as e:
        return {
            "original_query": query,
            "translated_query": query,  # Fallback to original
            "source_language": source_language or "unknown",
            "target_language": target_language,
            "translation_success": False,
            "error": str(e),
            "provider": "OpenAI",
        }


def translate_multilingual_queries(
    queries: List[str], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Translate multiple queries for multilingual search.

    Args:
        queries: List of query strings to translate
        target_language: Target language code

    Returns:
        List of translation results
    """
    results = []
    for query in queries:
        result = translate_query_for_search(query, target_language)
        results.append(result)
    return results


def prepare_multilingual_search(
    query: str, documents: List[str], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Prepare query and documents for multilingual semantic search.

    Args:
        query: Search query string
        documents: List of document strings
        target_language: Target language for translation

    Returns:
        Dict containing prepared search data
    """
    # Translate query
    query_translation = translate_query_for_search(query, target_language)

    # Translate documents (first 5 for efficiency)
    sample_documents = documents[:5] if len(documents) > 5 else documents
    document_translations = translate_multilingual_queries(
        sample_documents, target_language
    )

    # Determine if translation is needed
    needs_translation = query_translation["source_language"] != target_language

    preparation = {
        "original_query": query,
        "translated_query": query_translation["translated_query"],
        "query_language": query_translation["source_language"],
        "target_language": target_language,
        "needs_translation": needs_translation,
        "translation_success": query_translation["translation_success"],
        "sample_document_translations": document_translations,
        "total_documents": len(documents),
        "provider": "OpenAI",
    }

    return preparation
