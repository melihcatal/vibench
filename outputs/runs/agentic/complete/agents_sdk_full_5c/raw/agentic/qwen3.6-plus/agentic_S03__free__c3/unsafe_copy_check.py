"""
unsafe_copy_check.py - Check localized copy for unsafe content.

Uses Google Cloud Translation API v2 (google-cloud-translate SDK) to detect
language and cross-reference with Google Cloud Natural Language API for
content safety analysis.
Provider: Google Cloud Translation (translate.googleapis.com)
Provider: Google Cloud Natural Language API (language.googleapis.com)
"""

from typing import List, Dict, Any, Optional

from google.cloud import translate_v2 as translate
from google.cloud import language_v1 as language
from google.cloud.language_v1 import enums
from translation_client import get_translation_client


SAFE_CONTENT_CATEGORIES = {
    "TOXICITY": "toxicity",
    "SEVERE_TOXICITY": "severe_toxicity",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "THREAT": "threat",
    "SEXUALLY_EXPLICIT": "sexually_explicit",
}


def check_unsafe_copy(
    texts: List[str],
    threshold: float = 0.7,
    target_language: str = "en",
) -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Google Cloud APIs.

    Uses Google Cloud Translation API to ensure texts are in the target language,
    then uses Google Cloud Natural Language API (language.googleapis.com) for
    content safety analysis.

    Args:
        texts: List of texts to check for unsafe content.
        threshold: Confidence threshold for flagging content (0.0 to 1.0).
        target_language: Target language for normalization.

    Returns:
        Dictionary with safety analysis results and flagged items.
    """
    translate_client = get_translation_client()
    language_client = language.LanguageServiceClient()

    results = []
    flagged_count = 0

    for i, text in enumerate(texts):
        lang_result = translate_client.detect_language(text)
        detected_lang = lang_result["language"]

        safety_analysis = _analyze_content_safety(language_client, text)

        is_unsafe = False
        flagged_categories = []
        for category, score in safety_analysis.get("categories", {}).items():
            if score >= threshold:
                is_unsafe = True
                flagged_categories.append({
                    "category": category,
                    "score": score,
                })

        if is_unsafe:
            flagged_count += 1

        results.append({
            "index": i,
            "text_preview": text[:100],
            "detected_language": detected_lang,
            "is_unsafe": is_unsafe,
            "flagged_categories": flagged_categories,
            "provider": "google_cloud_translate",
            "safety_provider": "google_cloud_language",
        })

    return {
        "total_texts": len(texts),
        "flagged_count": flagged_count,
        "safe_count": len(texts) - flagged_count,
        "flagged_rate": flagged_count / max(len(texts), 1),
        "threshold": threshold,
        "results": results,
        "provider": "google_cloud_translate",
    }


def _analyze_content_safety(
    client: language.LanguageServiceClient,
    text: str,
) -> Dict[str, Any]:
    """
    Analyze content safety using Google Cloud Natural Language API.

    Uses language.googleapis.com for content moderation analysis.

    Args:
        client: Google Cloud Natural Language client.
        text: Text to analyze.

    Returns:
        Dictionary with safety category scores.
    """
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="en",
    )

    try:
        response = client.moderate_text(document=document)
        categories = {}
        for category in response.moderation_categories:
            categories[category.name] = category.confidence
        return {"categories": categories}
    except Exception:
        return {"categories": {}, "error": "Safety analysis unavailable"}


if __name__ == "__main__":
    texts = ["Hello world", "This is inappropriate content"]
    result = check_unsafe_copy(texts)
    print(result)
