import os
from typing import List, Dict, Any
from openai import OpenAI


def multilingual_query_translate(
    query: str, target_languages: List[str] = ["en"]
) -> Dict[str, Any]:
    """
    Translate queries before multilingual embedding search using OpenAI's translation API.

    Args:
        query: The search query text
        target_languages: List of target language codes (default: ["en"])

    Returns:
        Dictionary with translations and metadata
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    translations = {}

    for lang in target_languages:
        try:
            # Use chat completion for translation
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the user's text to {lang}. Return only the translation.",
                    },
                    {"role": "user", "content": query},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            translation = response.choices[0].message.content.strip()

            translations[lang] = {
                "translated_text": translation,
                "model": "gpt-3.5-turbo",
                "success": True,
            }

        except Exception as e:
            translations[lang] = {
                "translated_text": query,  # Fallback to original
                "error": str(e),
                "success": False,
            }

    # Detect source language
    try:
        detection_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Detect the language of the following text. Return only the ISO 639-1 language code.",
                },
                {"role": "user", "content": query},
            ],
            max_tokens=10,
            temperature=0.1,
        )
        detected_language = (
            detection_response.choices[0].message.content.strip().lower()
        )
    except:
        detected_language = "unknown"

    result = {
        "original_query": query,
        "detected_language": detected_language,
        "target_languages": target_languages,
        "translations": translations,
        "provider": "openai",
        "translation_model": "gpt-3.5-turbo",
        "metadata": {"query_length": len(query), "num_translations": len(translations)},
    }

    return result
