import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


def translate_query_for_multilingual_search(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate queries before multilingual embedding search using DeepL API.

    Args:
        query: The search query string
        target_language: Target language code (default: "en" for English)
        source_language: Optional source language code (auto-detected if None)

    Returns:
        Dict with translation results
    """
    # Using DeepL API for translation
    deepl_api_key = os.environ.get("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError(
            "DEEPL_API_KEY environment variable is required for translation"
        )

    import requests

    # DeepL API endpoint
    url = "https://api-free.deepl.com/v2/translate"

    params = {
        "auth_key": deepl_api_key,
        "text": query,
        "target_lang": target_language.upper(),
    }

    if source_language:
        params["source_lang"] = source_language.upper()

    try:
        response = requests.post(url, data=params)
        response.raise_for_status()

        translation_data = response.json()

        if "translations" in translation_data and translation_data["translations"]:
            translation = translation_data["translations"][0]

            result = {
                "original_query": query,
                "translated_query": translation["text"],
                "source_language": translation.get(
                    "detected_source_language", source_language or "auto"
                ),
                "target_language": target_language,
                "translation_provider": "DeepL",
                "success": True,
            }

            # Get language name mapping
            language_names = {
                "EN": "English",
                "ES": "Spanish",
                "FR": "French",
                "DE": "German",
                "IT": "Italian",
                "PT": "Portuguese",
                "NL": "Dutch",
                "PL": "Polish",
                "RU": "Russian",
                "JA": "Japanese",
                "ZH": "Chinese",
                "KO": "Korean",
                "AR": "Arabic",
                "HI": "Hindi",
                "TR": "Turkish",
                "SV": "Swedish",
                "DA": "Danish",
                "FI": "Finnish",
                "EL": "Greek",
                "CS": "Czech",
                "HU": "Hungarian",
                "RO": "Romanian",
                "SK": "Slovak",
                "BG": "Bulgarian",
            }

            source_code = result["source_language"].upper()
            target_code = target_language.upper()

            result["source_language_name"] = language_names.get(
                source_code, source_code
            )
            result["target_language_name"] = language_names.get(
                target_code, target_code
            )

            return result

        else:
            return {
                "original_query": query,
                "translated_query": query,  # Fallback to original
                "source_language": source_language or "unknown",
                "target_language": target_language,
                "translation_provider": "DeepL",
                "success": False,
                "error": "No translation returned from API",
            }

    except Exception as e:
        # Fallback to original query if translation fails
        return {
            "original_query": query,
            "translated_query": query,
            "source_language": source_language or "unknown",
            "target_language": target_language,
            "translation_provider": "DeepL",
            "success": False,
            "error": str(e),
        }


def translate_multilingual_queries(
    queries: List[str],
    target_language: str = "en",
    source_languages: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Translate multiple queries for multilingual search.

    Args:
        queries: List of query strings
        target_language: Target language code
        source_languages: Optional list of source language codes (one per query)

    Returns:
        List of translation results
    """
    results = []

    for i, query in enumerate(queries):
        source_lang = (
            source_languages[i]
            if source_languages and i < len(source_languages)
            else None
        )

        translation_result = translate_query_for_multilingual_search(
            query=query, target_language=target_language, source_language=source_lang
        )

        results.append(translation_result)

    return results


def prepare_multilingual_search(
    query: str, documents: List[str], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Prepare query and documents for multilingual embedding search.

    Args:
        query: Search query string
        documents: List of document strings
        target_language: Target language for translation

    Returns:
        Dict with prepared search data
    """
    # Translate query
    query_translation = translate_query_for_multilingual_search(query, target_language)

    # Note: In a real scenario, you might also translate documents
    # For now, we assume documents are already in the target language
    # or we use multilingual embedding models that handle multiple languages

    preparation = {
        "original_query": query,
        "translated_query": query_translation["translated_query"],
        "translation_success": query_translation["success"],
        "target_language": target_language,
        "documents_count": len(documents),
        "multilingual_capable": True,
        "notes": [
            "Using multilingual embedding model for cross-language search",
            "Query translated for consistency with document language",
            "Consider using text-embedding-3-multilingual models if available",
        ],
    }

    if not query_translation["success"]:
        preparation["warnings"] = [
            "Query translation failed, using original query",
            "Search quality may be reduced for cross-language queries",
        ]

    return preparation
