from google.cloud import language_v1
from typing import List, Dict


def analyze_script_safety(text_content: str) -> List[Dict]:
    """Checks narration scripts for unsafe content using Google Cloud Natural Language API (content classification).

    Args:
        text_content: The script text to analyze.

    Returns:
        A list of dictionaries, each containing 'category_name' and 'confidence' for detected content categories.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={"document": document})

    safety_results = []
    for category in response.categories:
        safety_results.append(
            {
                "category_name": category.name,
                "confidence": category.confidence,
            }
        )
    return safety_results
