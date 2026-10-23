import os
from typing import List, Dict, Any
from google.cloud import language_v1

def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Checks corpus text for safety attributes using Google Cloud Language API's Classify Text.

    Note: For more advanced and direct harmful content detection, Google Cloud's Vertex AI
    Safety API should be considered. This implementation uses the general purpose
    Language API's classification as a proxy for basic safety checks.

    Args:
        texts: A list of text strings to check.

    Returns:
        A dictionary containing safety analysis results for each text.
    """
    client = language_v1.LanguageServiceClient()
    results = {}

    for i, text in enumerate(texts):
        if not text.strip():
            results[f"text_{i}"] = {"status": "skipped", "reason": "empty text"}
            continue

        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )

        try:
            # The classify_text method is typically used for general content classification.
            # While not a dedicated safety API, it can identify categories that might be related
            # to harmful content (e.g., "Adult", "Violence").
            response = client.classify_text(document=document)
            categories = []
            for category in response.categories:
                categories.append({
                    "name": category.name,
                    "confidence": category.confidence
                })
            results[f"text_{i}"] = {"status": "analyzed", "categories": categories}
        except Exception as e:
            results[f"text_{i}"] = {"status": "error", "message": str(e)}

    return results
